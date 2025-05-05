<p align="center">
  <img src=https://github.com/user-attachments/assets/b8524ce9-a1fc-4005-98da-5dbf6be4000d>
  <br/>
  <strong>A set of novel HCI workflows for interacting with LLMs</strong>
</p>

# screen-query, sd-picker and sqa
**The tmux suite**:
This is a conversational agent with suppport for conversation history, adding screenshots, command output, cycling pane focus, wiping memory, turning off and on pane capturing, adding external context... 

There's an intentionally unsophisticated `installer.sh` that may work and if it doesn't, it should be very easy to find out what's going on.

[demo.webm](https://github.com/user-attachments/assets/9e8dd99a-510b-4708-9ab5-58b75edf5945)

You should also use `sqa` which can pipe anything into the context. Here's an example:
![out](https://github.com/user-attachments/assets/62318080-9d67-41de-921b-976ad61e1122)

You need a modernish version of [fzf](https://github.com/junegunn/fzf), [streamdown](https://github.com/kristopolous/Streamdown) and [simonw's llm](https://github.com/simonw/llm). You can use it for free via openrouter.

Once you're in there's a few slash commands. These are all dumb - there's no tab completion or anything fancy. Just enter `/help` to get the current list.

![2025-05-01_13-38](https://github.com/user-attachments/assets/e57ea643-cb63-4727-9901-e15109b81adb)



Here's some screenshots:
![2025-04-26_18-45](https://github.com/user-attachments/assets/a81cbcea-cb15-46d9-92ac-5430238b2b85)

![2025-04-26_18-49](https://github.com/user-attachments/assets/c8b98e30-cd09-47bc-b751-02a929a82703)

![2025-04-26_18-49_1](https://github.com/user-attachments/assets/c752f94f-b780-4a8b-b597-1ce62b2bdb78)

The program, screen-query is meant to be really simple. Modify it as needed.

# kb-capture.py and llm-magic
**The xorg suite**:
`kb-capture.py` captures keyboard events from an X server and converts them into a string.  It exits and prints the captured string when a semicolon (`;`) or colon (`:`) is pressed. `llm-magic` is a shell script that uses `kb-capture.py` to capture keyboard input, sends it to an LLM for processing, and displays the LLM's response using `dzen2` and then types it out using xdotool. 

Their powers combined gives you llm prompting in any application. Here I am 

 * ssh'ing to a remote machine
 * using a classic text editor (scite)
 * using classic vim

I do a keystroke to invoke `llm-magic`, type my request, then ; and it replaces my query with the response. Totally magic. Just like it says. 

![out](https://github.com/user-attachments/assets/07ed72d0-87ef-4270-b880-ae8797bd8c4e)

# wtf.zsh 
A tool designed to read a directory of files, describe their content, categorize their purposes and answer basic questions. Example!

![un](https://github.com/user-attachments/assets/0fe52d11-cf79-45e1-ba3c-4bbbfba81610)

# shell-hook.zsh
A Zsh shell hook that intercepts user input *before* execution. It constructs a detailed prompt including system information and the user's input, sends this to an LLM, and replaces the user's input with the LLM's response.  It reads the default LLM model from `~/.config/io.datasette.llm/default_model.txt`.

This is probably the most used tool of all of them. I use it probably 10-20 times a day. ffmpeg, ssh port forwarding, openssl certificate checking, jq stuff ... this one is indispensible
![out](https://github.com/user-attachments/assets/01488c16-fb68-4fdb-a7ea-76e12499641d)


## Future work

There's interesting terminals called [waveterm](https://www.waveterm.dev/) and [warp](https://www.warp.dev/) basically an i3/tmux merge point with some kind of chat built in to the side. Then there's this IDE called [windsurf](https://windsurf.com/editor) that looks at your behavior as you navigate around. The idea here, is to extend screen-query to be a less clunky version of [ai-chat](https://github.com/sigoden/aichat) that looks at your various tmux panes, uses [procfs](https://en.wikipedia.org/wiki/Procfs) to be a paired programmer. The problem with things like [aider](https://aider.chat/), [plandex](https://plandex.ai/) [codex](https://github.com/openai/codex) and [goose](https://github.com/block/goose) is it takes on too much of a role, as opposed to being a tool it tries to be a junior dev - taking on too much responsibility, making bad assumptions, and creating messes. 

I think I synthesized this on this HN comment on 2025-04-19: 

> I found that if I'm unfamiliar with the knowledge domain I'm mostly using AI but then as I dive in the ratio of AI to human changes to the point where it's AI at 0 and it's all human.
> Basically AI wins at day 1 but isn't any better at day 50. If this can change then it's the next step.

You can see this in the featured demos. They are all "starting from 0" points of unblocking yourself. This is great. You won't do anything until you convince yourself it's easy. But the core objective of screen-query at this point, and the thing I'm excited about is moving beyond that.

As human knowledge (and opinion) progresses, ai needs to plays a "co" role - co-expert, co-craftsman, co-reference. Take the [streamdown](https://github.com/kristopolous/Streamdown) project I mentioned before. As time progressed and I discovered more subtle bugs, I found that they were inserted by the vibe-coding AI I did early on to get myself started. The percentage of the code that is AI basically went from maybe 90% on first commit to perhaps 10% now, where it's slowly asymptotically decreasing because it continues to be able to only make what I call Day-0 or Day-1 contributions to a project I've reached Day-30 on.

The fidelity of this nuance has to be crisp without introducing the noise and the context of the HCI will get us there. That's where screen-query is going next.

It's not just prompting a single llm. Take [teapot](https://huggingface.co/teapotai/teapotllm) for example - there's many models that excel at certain modalities of interaction. The key is to slot these multi-agents into a proper stack using things such as file contents, commit histories, documentation, tests, and user interaction to get past Day-0/1 contributions and stop producing coding slop when quality starts mattering. agno in March 2025 attempted to address this through the roles abstraction and it's probably the right 1.0

There's a famous 2019 essay called [the bitter lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) about how sophistication of models and complexity of solution are simply getting out-classed by naive "more compute" solutions. This is not that. These problems require problem contextualization and more nuanced presumptions with more clever AI can't get you there. This is wildly observable in humans. There is no human that can just sit down at a company and be productive on day 1 of a complex project, making meaningful contributions. Maximizing the utility of AI requires it to play a codependent fluid dynamic role with the human throughout the creative process

All code is institutional and all institutions are collective behavior and all behaviors are learned and poorly documented. Therein lies the next step-change

~chris 2025-04-20
