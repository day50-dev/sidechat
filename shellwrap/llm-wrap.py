#!/bin/bash
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "toml"
# ]
# ///
'''':
if command -v uv &> /dev/null; then
    exec uv run --script "$0" "$@"
else
    exec python3 "$0" "$@"
fi
'''
import os
import pty
import select
import sys
import argparse
import tempfile
import tty
import termios
import fcntl
import re
import subprocess 
from io import StringIO
import openai # openai v1.0.0+

CLIENT = openai.OpenAI(api_key="anything",base_url="http://0.0.0.0:4000") # set proxy to base_url
ESCAPE = b'\x18'  # ctrl+x
PATH_INPUT = None
PATH_OUTPUT = None
ANSIESCAPE = r'\033(?:\[[0-9;?]*[a-zA-Z]|][0-9]*;;.*?\\|\\)'
strip_ansi = lambda x: re.sub(ANSIESCAPE, "", x)

SYSTEMPROMPT = """
You are an experienced Linux engineer with expertise in all Linux commands and their functionality across different Linux systems.
The format for the request is:
<input>
(The previous users input)
</input>
<query>
(The current user input)
</query>
<screen>
(What the user sees on the screen)
</screen>
For instance, the output may have something like the output of the previous command + the current prompt. The input should have a question. Your job is to
use the <screen> to establish the context and answer the <input>,
Generate a single command or a pipeline of commands that accomplish the task efficiently. The user may be in something other than the shell such as
ipython, psql, sqlite, etc. Use the <screen> to determine the context.
Output only the command as a single line of plain text, with no quotes, formatting, or additional commentary. Do not use markdown or any
other formatting. Do not include the command into a code block.
Don't include the prompt itself the command. The user query is in the <query> tag.
"""

parser = argparse.ArgumentParser(description='llm-wrap script')
parser.add_argument('--method', choices=['litellm', 'simonw', 'vllm'], default='litellm', help='Method to use for LLM interaction')
parser.add_argument('--exec', '-e', dest='exec_command', help='Command to execute')
args = parser.parse_args()

def clean_input(raw_input):
    fake_stdin = StringIO(raw_input.decode('utf-8'))
    sys.stdin = fake_stdin
    processed_input = input()
    sys.stdin = sys.__stdin__
    return processed_input

def activate(qstr):
    with open(PATH_INPUT, "rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(max(0, size - 500), os.SEEK_SET)
        recent_input = f.read()

    processed_input = clean_input(recent_input)

    with open(PATH_OUTPUT, "rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(max(0, size - 500), os.SEEK_SET)
        recent_output = strip_ansi(f.read().decode('utf-8'))

    request_string = f"<input>{processed_input}</input><output>{recent_output}</output>"
    
    if args.method == 'litellm':
        response = CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages = [
            {
                "role": "system",
                "content": SYSTEMPROMPT
            },
            {
                "role": "user",
                "content": request_string
            }
        ])
        print(response.output_text)

    elif args.method == 'simonw':
        systemprompt = SYSTEMPROMPT.replace("\"", "\\\"")
        command = f'llm -x -s "{systemprompt}" "{request_string}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output

    elif args.method == 'vllm':
        print("vllm method selected")

    
def set_pty_size(fd, target_fd):
    s = fcntl.ioctl(target_fd, termios.TIOCGWINSZ, b"\x00" * 8)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, s)

def main():
    global PATH_INPUT, PATH_OUTPUT
    temp_dir = tempfile.mkdtemp(dir="/tmp/screen-query")
    os.makedirs(temp_dir, exist_ok=True)
    PATH_INPUT = os.path.join(temp_dir, "input")
    PATH_OUTPUT = os.path.join(temp_dir, "output")
    print(f"Input path: {PATH_INPUT}")
    print(f"Output path: {PATH_OUTPUT}")
    is_escaped = False
    ansi_pos = None
    qstr = b''

    orig_attrs = termios.tcgetattr(sys.stdin.fileno())
    try:
        tty.setraw(sys.stdin.fileno())  # raw mode to send Ctrl-C, etc.
        pid, fd = pty.fork()

        if pid == 0:
            print(args.exec_command)
            exec_command_list = args.exec_command.split()
            os.execvp(exec_command_list[0], exec_command_list)
        else:
            set_pty_size(fd, sys.stdin.fileno())

            while True:
                r, _, _ = select.select([fd, sys.stdin], [], [])

                if sys.stdin in r:
                    user_input = os.read(sys.stdin.fileno(), 1024)
                    if not user_input:
                        break
                    
                    if is_escaped:
                        qstr += user_input
                   
                        if b'\r' in user_input:
                            is_escaped = False
                            sys.stdout.write('\x1b[8m')
                            sys.stdout.flush()
                            # AI: restore the ansi position
                            os.write(sys.stdout.fileno(), '\x1b[u'.encode())
                            command = activate(qstr)
                            os.write(fd, command)
                            sys.stdout.flush()

                            # AI: restore the ansi position
                            #os.write(sys.stdout.fileno(), '\x1b[u'.encode())
                            continue

                    if ESCAPE in user_input:
                        is_escaped = True
                        #AI: save the ansi position here
                        ansi_pos = '\x1b[s'
                        os.write(sys.stdout.fileno(), ansi_pos.encode())

                        sys.stdout.write('\x1b[7m >> ') 
                        sys.stdout.flush()
                        continue
                
                    with open(PATH_INPUT, "ab") as f:
                        f.write(user_input)
                        f.flush()

                    if is_escaped:
                        os.write(sys.stdout.fileno(), user_input)
                    else:
                        os.write(fd, user_input)

                if fd in r:
                    output = os.read(fd, 1024)
                    if not output:
                        break

                    with open(PATH_OUTPUT, "ab") as f:
                        f.write(output)
                        f.flush()

                    os.write(sys.stdout.fileno(), output)
                    #os.write(sys.stdout.fileno(), b''.join(chunks))

    except (OSError, KeyboardInterrupt):
        print("\n\rExiting...")
        sys.exit(130)

    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, orig_attrs)

if __name__ == "__main__":
    main()
