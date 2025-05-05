<p align="center">
  <img src=https://github.com/user-attachments/assets/b8524ce9-a1fc-4005-98da-5dbf6be4000d>
  <br/>
  <strong>A set of hackable novel HCI tools for workflows with LLMs</strong>
</p>

This is a variety of tools broken up into three fun parties:
 * **[Tmux Talkers](#the-tmux-talkers)**: A sidebar chat interface for tmux
 * **[Xorg Xtractors](#the-xorg-xtractors)**: LLM interception and injection at the Xorg level
 * **[Shell Snoopers](#the-shell-snoopers)**: Similar tools but done at the shell and terminal I/O level

### But wait! 
To use anything here you'll need a modernish version of [streamdown](https://github.com/kristopolous/Streamdown) and [simonw's llm](https://github.com/simonw/llm). [fzf](https://github.com/junegunn/fzf) is also needed for the talkers!

## The Tmux Talkers

**screen-query, sq-picker and sq-add**

An llm intervention in your little terminal with suppport for adding screenshots, command output, cycling pane focus, wiping memory, history, turning off and on pane capturing, adding external context and probably more after I write this, all sitting agnostically on top of tmux so there's no substantive workflow change needed. You can just beckon your trusty friend at your leisure.

There's an intentionally unsophisticated `installer.sh` that may work and if it doesn't, it should be very easy to find out what's going on.

[demo.webm](https://github.com/user-attachments/assets/9e8dd99a-510b-4708-9ab5-58b75edf5945)

You should also use `sq-add` which can pipe anything into the context. Here's an example:
![out](https://github.com/user-attachments/assets/62318080-9d67-41de-921b-976ad61e1122)


Once you're in there's a few slash commands. Use `/help` to get the current list.

Multiline is available with backslash `\`, just like it is at the shell

![2025-05-01_13-38](https://github.com/user-attachments/assets/e57ea643-cb63-4727-9901-e15109b81adb)


Here's some screenshots of how it seamlessly works with Streamdown's built in `Savebrace` feature and how it helps workflow.
![2025-04-26_18-45](https://github.com/user-attachments/assets/a81cbcea-cb15-46d9-92ac-5430238b2b85)

![2025-04-26_18-49](https://github.com/user-attachments/assets/c8b98e30-cd09-47bc-b751-02a929a82703)

![2025-04-26_18-49_1](https://github.com/user-attachments/assets/c752f94f-b780-4a8b-b597-1ce62b2bdb78)

## The Xorg Xtractors

**kb-capture.py and llm-magic**

`kb-capture.py` captures keyboard events from an X server and converts them into a string.  It exits and prints the captured string when a semicolon (`;`) or colon (`:`) is pressed. `llm-magic` is a shell script that uses `kb-capture.py` to capture keyboard input, sends it to an LLM for processing, and displays the LLM's response using `dzen2` and then types it out using xdotool. 

Their powers combined gives you llm prompting in any application. Here I am 

 * ssh'ing to a remote machine
 * using a classic text editor (scite)
 * using classic vim

I do a keystroke to invoke `llm-magic`, type my request, then ; and it replaces my query with the response. Totally magic. Just like it says. 

![out](https://github.com/user-attachments/assets/07ed72d0-87ef-4270-b880-ae8797bd8c4e)

## The Shell Snoopers 

**shell-hook, shellwrap and wtf**

### shell-hook.zsh
A Zsh shell hook that intercepts user input before execution. It constructs a detailed prompt including system information and the user's input, sends this to an LLM, and replaces the user's input with the LLM's response. 

This is probably the most used tool of all of them. I use it probably 10-20 times a day. ffmpeg, ssh port forwarding, openssl certificate checking, jq stuff ... this one is indispensible
![out](https://github.com/user-attachments/assets/01488c16-fb68-4fdb-a7ea-76e12499641d)

### shellwrap
shellwrap is a new concept, generally. It shepherds your input and output as a true wrapper and logs both sides of the conversation into files. Then when you invoke the llm it will pre-empt any existing interaction, kind of like the ssh shell escape. This is what the reversed triangle input in the video is. That's invoked with a keyboard shortcut, currently `ctrl+x`.

Then you type your command in and press enter. This command, plus the context of your previous input and output is then sent off to the llm and its response is wired up to the stdin of the application.

So for instance, 
 * I'm inside my zsh shell and it gives me shell commands.
 * Then I go inside of a full screen program, in this case vim. I pre-empt the vim session and just start typing. The llm infers it's vim and knows what mode I'm in from my previous keystrokes and correctly exits.
 * I give it a prompt at the python shell and it uses the context to infer it and then to my request in a compatible way.

This works seamlessly over ssh boundaries, in visual applications, at REPLs --- anywhere.

[shellwrap1.webm](https://github.com/user-attachments/assets/29530ecf-15b6-4db1-9928-302c8674228e)

### wtf
A tool designed to read a directory of files, describe their content, categorize their purposes and answer basic questions. Example!

(Notice how it has no idea what shellwrap does. Told you it was new! ;-) )

![un](https://github.com/user-attachments/assets/0fe52d11-cf79-45e1-ba3c-4bbbfba81610)

## Future work

see [the wiki](https://github.com/kristopolous/llmehelp/wiki)
