import os
import pty
import select
import sys
import tty
import termios
import fcntl
import struct

def set_pty_size(fd, target_fd):
    """Set window size of PTY to match the real terminal."""
    s = fcntl.ioctl(target_fd, termios.TIOCGWINSZ, b"\x00" * 8)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, s)

def main():
    # Save original terminal settings
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
                    os.write(fd, user_input)

                if fd in r:
                    output = os.read(fd, 1024)
                    if not output:
                        break

                    # Carefully handle ANSI sequences
                    # Split on ANSI escape sequences to avoid breaking them
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
                            # Perform replacement on plain text only
                            text = output[i:j].replace(b"fizz", b"fizzbuzz")
                            chunks.append(text)
                            i = j

                    os.write(sys.stdout.fileno(), b''.join(chunks))

    except (OSError, KeyboardInterrupt):
        sys.exit(130)

    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, orig_attrs)

if __name__ == "__main__":
    main()

