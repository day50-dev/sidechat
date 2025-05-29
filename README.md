<p align="center">
  <img src=https://github.com/user-attachments/assets/b8524ce9-a1fc-4005-98da-5dbf6be4000d>
  <br/>
  <strong>Hackable HCI tools to fix all those AI bugs</strong>
</p>

An AI-first, privacy respecting, integrated diagnostic and development suite built the Unix way, through small tools that can be orchestrated together.

 * **[Tmux Talkers](#the-tmux-talkers)**: A sidebar chat in tmux
 * **[Shell Snoopers](#the-shell-snoopers)**: Tiny tools for shining up your shell
 * **[Xorg Xtractors](#the-xorg-xtractors)**: LLM interception and injection in your Xorg

## The Tmux Talkers

**screen-query, sq-picker and sq-add**

Simple installer:

    curl day50.dev/talker | sh

An llm intervention in your little terminal with suppport for adding screenshots, command output, cycling pane focus, turning off and on pane capturing, adding external context and more, all sitting agnostically on top of tmux so there's no substantive workflow change needed. You can just beckon your trusty friend at your leisure.


[demo.webm](https://github.com/user-attachments/assets/9e8dd99a-510b-4708-9ab5-58b75edf5945)

## There's an agentic mode. We call it DUI. Enable it with `/dui`.
![2025-05-15_18-50](https://github.com/user-attachments/assets/d1da6063-b450-49f8-863d-fcf0c32647fc)



You should also use `sq-add` which can pipe anything into the context. Here's an example:
![out](https://github.com/user-attachments/assets/62318080-9d67-41de-921b-976ad61e1122)


Once you're in there's a few slash commands. Use `/help` to get the current list.

Multiline is available with backslash `\`, just like it is at the shell

![2025-05-01_13-38](https://github.com/user-attachments/assets/e57ea643-cb63-4727-9901-e15109b81adb)


Here's some screenshots of how it seamlessly works with [Streamdown's](https://github.com/day50-dev/Streamdown) built in `Savebrace` feature and how it helps workflow.
![2025-04-26_18-45](https://github.com/user-attachments/assets/a81cbcea-cb15-46d9-92ac-5430238b2b85)

![2025-04-26_18-49](https://github.com/user-attachments/assets/c8b98e30-cd09-47bc-b751-02a929a82703)

![2025-04-26_18-49_1](https://github.com/user-attachments/assets/c752f94f-b780-4a8b-b597-1ce62b2bdb78)

Also you don't need `tmux`! Often you'll be doing things and then realize you want the talk party and you're not in tmux.

That's fine! If you use [streamdown](https://github.com/day50-dev/Streamdown),  `sq-picker` works like it does inside tmux. You can also `sq-add` by id. It's not great but you're not locked in. That's the point!

## The Shell Snoopers 

**shell-hook, shellwrap and wtf**

### Shell-hook.zsh

Moved to [Zummoner](https://github.com/day50-dev/Zummoner).

### Shellwrap

Moved to [ESChatch](https://github.com/day50-dev/ESChatch).

### WTF
A tool designed to read a directory of files, describe their content, categorize their purposes and answer basic questions. Example!

(Notice how it has no idea what shellwrap does. Told you it was new! ;-) )

![un](https://github.com/user-attachments/assets/0fe52d11-cf79-45e1-ba3c-4bbbfba81610)

## The Xorg Xtractors

**kb-capture.py and llm-magic**

`kb-capture.py` captures keyboard events from an X server and converts them into a string.  It exits and prints the captured string when a semicolon (`;`) or colon (`:`) is pressed. `llm-magic` is a shell script that uses `kb-capture.py` to capture keyboard input, sends it to an LLM for processing, and displays the LLM's response using `dzen2` and then types it out using xdotool. 

Their powers combined gives you llm prompting in any application. Here the user is

 * ssh'ing to a remote machine
 * using a classic text editor (scite)
 * using classic vim

I do a keystroke to invoke `llm-magic`, type my request, then ; and it replaces my query with the response. Totally magic. Just like it says. 

![out](https://github.com/user-attachments/assets/07ed72d0-87ef-4270-b880-ae8797bd8c4e)


Thanks for stopping by!
