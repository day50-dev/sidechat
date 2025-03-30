# llmehelp

This project aims to capture keyboard input and leverage a Large Language Model (LLM) to assist with tasks. It provides several tools for interacting with LLMs in different contexts.

## Files

*   **kb-capture.py:** A Python script that captures keyboard events using `python-xlib`. It records key presses and releases from an X server and converts them into a string.  It exits and prints the captured string when a semicolon (`;`) or colon (`:`) is pressed, and supports backspace functionality.

*   **llm-magic:** A shell script that uses `kb-capture.py` to capture keyboard input, sends it to an LLM for processing, and displays the LLM's response using `dzen2`. It includes a basic length check to prevent processing very short inputs.

*   **screen-query:** A script for interacting with a tmux session and an LLM. It captures the contents of a tmux pane, sends it to an LLM with a prompt, and displays the LLM's response using `mdreader` (or `cat` as a fallback). It also manages conversation history using a SQLite database.

*   **shell-hook.zsh:** A Zsh shell hook that intercepts user input *before* execution. It constructs a detailed prompt including system information and the user's input, sends this to an LLM, and replaces the user's input with the LLM's response.  It reads the default LLM model from `~/.config/io.datasette.llm/default_model.txt`.

*   **wrap.sh:** A wrapper script that combines `kb-capture.py` and `llm-magic`. It captures keyboard input, sends it to the LLM, and then types the LLM's response into the current context using `xdotool`.  This script is a simplified version of `llm-magic`.




