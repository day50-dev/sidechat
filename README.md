# llmehelp

This project aims to capture keyboard input and leverage a Large Language Model (LLM) to assist with tasks.

## Files

*   **kb-capture.py:** This Python script captures keyboard events using the `python-xlib` library. It connects to an X server, records key presses and releases, and converts them into strings. It includes a callback function that prints the captured string when a semicolon (`;`) or colon (`:`) is pressed, and allows for backspace functionality. It uses two X displays, `local_display` and `record_display`.

*   **llm-magic:** This shell script captures keyboard input using `kb-capture.py`, sends it to an LLM for processing, and then outputs the LLM's response using `dzen2` for display. It also includes logic to handle short inputs (aborting if the input is less than 10 characters). It kills the `dzen2` process after the LLM response is received.

*   **screen-query:** For interacting with a tmux session and an LLM. It can capture the contents of a tmux pane, send it to an LLM along with a user prompt, and display the LLM's response using `mdreader` (which defaults to `cat` if `glow` or `sd.py` are not found). It also manages conversation history using a SQLite database.

*   **shell-hook.zsh:** This Zsh shell hook intercepts user input before it's executed. It constructs a prompt that includes system information and the user's input, sends this prompt to an LLM, and then replaces the user's input with the LLM's response. It uses a configuration file (`~/.config/io.datasette.llm/default_model.txt`) to determine the LLM model to use.

*   **wrap.sh:** This script is a wrapper around `kb-capture.py` and `llm-magic`. It captures keyboard input using `kb-capture.py`, sends it to the LLM via `llm-magic`, and then types the LLM's response into the current context using `xdotool`.


