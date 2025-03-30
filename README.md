# llmehelp

This is really my LLM terminal demo suite. It includes 3 basic things:

* X input interception (kb-capture.py + llm-magic)
* zsh interception (shell-hook.zsh)
* tmux screen share and chat (screen-query)

Unlike aider/goose/claude desktop, these are llm micro-helpers, designed to help you in a pinch instead of turn you into a manager and code reviewer of an junior dev AI assistant - not that there's anything wrong with that - I use them as well.

If you aren't using my [streamdown](https://github.com/kristopolous/Streamdown) project with these for streaming markdown rendering in the browser, you're doing it wrong.

These are designed to work in linux, under Xorg. There's a dzen2 dependency with the llm-magic and simonw's llm script for all of them.

## Files

*   **kb-capture.py:** A Python script that captures keyboard events using `python-xlib`. It records key presses and releases from an X server and converts them into a string.  It exits and prints the captured string when a semicolon (`;`) or colon (`:`) is pressed, and supports backspace functionality.

*   **llm-magic:** A shell script that uses `kb-capture.py` to capture keyboard input, sends it to an LLM for processing, and displays the LLM's response using `dzen2` and then types it out using xdotool. 

*   **screen-query:** A script for interacting with a tmux session and an LLM. It captures the contents of a tmux pane, sends it to an LLM with a prompt, and displays the LLM's response using `mdreader` (or `cat` as a fallback). It also manages conversation history using a SQLite database.

*   **shell-hook.zsh:** A Zsh shell hook that intercepts user input *before* execution. It constructs a detailed prompt including system information and the user's input, sends this to an LLM, and replaces the user's input with the LLM's response.  It reads the default LLM model from `~/.config/io.datasette.llm/default_model.txt`.





