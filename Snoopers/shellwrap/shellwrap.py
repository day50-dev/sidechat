#!/usr/bin/env python3
import os
import pty
import select
import sys
import argparse
import tty
import termios
import fcntl
import re
import subprocess 
from io import StringIO

CLIENT = None
ESCAPE = b'\x18'  # ctrl+x
PATH_INPUT = None
PATH_OUTPUT = None
ANSIESCAPE = r'\033(?:\[[0-9;?]*[a-zA-Z]|][0-9]*;;.*?\\|\\)'
strip_ansi = lambda x: re.sub(ANSIESCAPE, "", x)

parser = argparse.ArgumentParser(description='shell wrap, a transparent shell wrapper')
parser.add_argument('--method', choices=['litellm', 'simonw', 'vllm'], default='litellm', help='Method to use for LLM interaction')
parser.add_argument('--exec', '-e', dest='exec_command', help='Command to execute')
args = parser.parse_args()

if args.method == 'litellm':
    import openai # openai v1.0.0+
    CLIENT = openai.OpenAI(api_key="anything",base_url="http://0.0.0.0:4000") # litellm

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

    request = f"""You are an experienced fullstack software engineer with expertise in all Linux commands and their functionality 
Given a task, along with a sequence of previous inputs and screen scrape, generate a single line of commands that accomplish the task efficiently.
This command is to be executed in the current program which can be determined by the screen scrape
The screen scrape is 
----
{recent_output}
----
The recent input is {processed_input}
----
Take special care and look at the most recent part of the screen scrape. Pay attention to
things like the prompt style, welcome banners, and be sensitive if the person is say at 
a python prompt, ruby prompt, gdb, or perhaps inside a program such as vim.

Create a command to accomplish the following task: {qstr.decode('utf-8')}

If there is text enclosed in paranthesis, that's what ought to be changed

Output only the command as a single line of plain text, with no
quotes, formatting, or additional commentary. Do not use markdown or any
other formatting. Do not include the command into a code block.
Don't include the program itself (bash, zsh, etc.) in the command.
"""

    if args.method == 'litellm':
        response = CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages = [
            {
                "role": "system",
                "content": SYSTEMPROMPT
            },
            {
                "role": "user",
                "content": request
            }
        ])
        print(response.output_text)

    elif args.method == 'simonw':
        command = f'llm -x "{request}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        with open("/tmp/screen-query/log", "ab") as f:
            f.write(request.encode('utf-8') + b'\n(' + output + b')\n')
            f.flush()

        return output

    elif args.method == 'vllm':
        print("vllm method selected")

    
def set_pty_size(fd, target_fd):
    s = fcntl.ioctl(target_fd, termios.TIOCGWINSZ, b"\x00" * 8)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, s)

def main():
    global PATH_INPUT, PATH_OUTPUT
    temp_dir = "/tmp/screen-query"
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
                   
                        if re.search(r'[\r\n]', user_input.decode('utf-8')):
                            is_escaped = False
                            sys.stdout.write('◀\x1b[8m')
                            sys.stdout.flush()
                            command = activate(qstr)
                            os.write(sys.stdout.fileno(), '\x1b[u'.encode())
                            os.write(fd, command)
                            sys.stdout.flush()
                            qstr = b''
                            continue

                    if ESCAPE in user_input:
                        is_escaped = True
                        #AI: save the ansi position here
                        ansi_pos = '\x1b[s'
                        os.write(sys.stdout.fileno(), ansi_pos.encode())

                        sys.stdout.write('\x1b[7m▶') 
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
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, orig_attrs)
        print("\n\rExiting...")
        sys.exit(130)

    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, orig_attrs)

if __name__ == "__main__":
    main()
