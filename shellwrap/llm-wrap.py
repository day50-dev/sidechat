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
import tempfile
import tty
import termios
import fcntl
import re
from io import StringIO
import openai # openai v1.0.0+

CLIENT = openai.OpenAI(api_key="anything",base_url="http://0.0.0.0:4000") # set proxy to base_url
ESCAPE = b'\x18'  # ctrl+x
PATH_INPUT = None
PATH_OUTPUT = None
ANSIESCAPE = r'\033(?:\[[0-9;?]*[a-zA-Z]|][0-9]*;;.*?\\|\\)'
strip_ansi = lambda x: re.sub(ANSIESCAPE, "", x)

SYSTEMPROMPT = """
The format for the request is:
<input>
(The previous users input)
</input>
<output>
(What the user sees on the screen)
</output>
For instance, the output may have something like the output of the previous command + the current prompt. The input should have a question. Your job is to
use the <output> to establish the context and answer the <input>, which may include input prior to the question, such as previous commands. These can be
used to establish more context.
"""

def clean_input(raw_input):
    fake_stdin = StringIO(raw_input.decode('utf-8'))
    sys.stdin = fake_stdin
    processed_input = input()
    sys.stdin = sys.__stdin__
    return processed_input

def activate():
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

    # request sent to model set on litellm proxy, `litellm --model`
    response = CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages = [
        {
            "role": "system",
            "content": SYSTEMPROMPT
        },
        {
            "role": "user",
            "content": f"<input>{processed_input}</input><output>{recent_output}</output>"
        }
    ])
    print(response.output_text)
    sys.stdout.flush()
    
def set_pty_size(fd, target_fd):
    s = fcntl.ioctl(target_fd, termios.TIOCGWINSZ, b"\x00" * 8)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, s)

def main():
    temp_dir = tempfile.mkdtemp(dir="/tmp")
    os.makedirs(temp_dir, exist_ok=True)
    screen_query_dir = os.path.join(temp_dir, "screen-query")
    os.makedirs(screen_query_dir, exist_ok=True)
    globals()['PATH_INPUT'] = os.path.join(screen_query_dir, "input")
    globals()['PATH_OUTPUT'] = os.path.join(screen_query_dir, "output")

    orig_attrs = termios.tcgetattr(sys.stdin.fileno())
    try:
        tty.setraw(sys.stdin.fileno())  # raw mode to send Ctrl-C, etc.
        pid, fd = pty.fork()

        if pid == 0:
            print(sys.argv)
            os.execvp(sys.argv[1], sys.argv[1:])
        else:
            set_pty_size(fd, sys.stdin.fileno())

            while True:
                r, _, _ = select.select([fd, sys.stdin], [], [])

                if sys.stdin in r:
                    user_input = os.read(sys.stdin.fileno(), 1024)
                    if not user_input:
                        break
                    if ESCAPE in user_input:
                        activate()
                
                    with open(PATH_INPUT, "ab") as f:
                        f.write(user_input)
                        f.flush()
                    os.write(fd, user_input)

                if fd in r:
                    output = os.read(fd, 1024)
                    if not output:
                        break

                    with open(PATH_OUTPUT, "ab") as f:
                        f.write(output)
                        f.flush()
                    """
                    chunks = []
                    i = 0
                    while i < len(output):
                        if output[i:i+1] == b'\x1b':
                            end = i + 1
                            while end < len(output) and not (64 <= output[end] <= 126):
                                end += 1
                            end += 1  # include final letter
                            chunks.append(output[i:end])
                            i = end
                        else:
                            j = i
                            while j < len(output) and output[j:j+1] != b'\x1b':
                                j += 1
                            text = output[i:j].replace(b"fizz", b"fizzbuzz")
                            chunks.append(text)
                            i = j
                    """

                    os.write(sys.stdout.fileno(), output)
                    #os.write(sys.stdout.fileno(), b''.join(chunks))

    except (OSError, KeyboardInterrupt):
        sys.exit(130)

    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, orig_attrs)

if __name__ == "__main__":
    main()
