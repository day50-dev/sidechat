<p align="center">
  <img src=https://github.com/user-attachments/assets/929421a7-ef83-4ca6-b0d8-7c8942b5ce41>
  <br/>
  <strong>A tmux-based AI assistant</strong>
</p>

Simple installer:

    curl day50.dev/sidechat | sh

Sidechat is an LLM intervention in your little terminal. 

It suppports 

 * adding the following:
    * screenshots 
    * multiple panes as a stack.
    * command output 
    * external context
    * memories 
 * reading from multiple clipboards
 * tool calling
 * MCP
 * agentic loops
 * cycling pane focus
 * local and remote servers thanks to the [llcat](https://github.com/day50-dev/llcat) backend.
 * reading sections of manpages with [mansnip](https://github.com/day50-dev/Mansnip).
 * turning off and on pane capturing
 
**Sidechat** sits agnostically on top of tmux. There's no substantive workflow change needed. You can just beckon your trusty friend at your leisure. 

Unlike opencode and friends you don't have to edit a json file to use a local model nor do you have to violate the single-source-of-truth pattern and specify your own copy of the models that can be trivially found by using a basic end point. 

We also know that "local model" means "model I control the infra for" and not necessarily something running on the same exact computer. So when you enter server addresses they get maintained in a list you can toggle through. You can even leave notes in them (only the first space delimited field is used). It's almost like adults made it.

[demo.webm](https://github.com/user-attachments/assets/9e8dd99a-510b-4708-9ab5-58b75edf5945)

There's an agentic mode. We call it DUI. Enable it with `/dui`.
![2025-05-15_18-50](https://github.com/user-attachments/assets/d1da6063-b450-49f8-863d-fcf0c32647fc)


You should also use `sc-add` which can pipe anything into the context. Here's an example:
![out](https://github.com/user-attachments/assets/62318080-9d67-41de-921b-976ad61e1122)


Once you're in there's a few slash commands. Use `/help` to get the current list.

Multiline is available with backslash `\`, just like it is at the shell

![2025-05-01_13-38](https://github.com/user-attachments/assets/e57ea643-cb63-4727-9901-e15109b81adb)


There's lots of nice features. Here's the self-update. As you can see it will
 * install the update
 * replace itself
 * pick up where you left off


Here's some screenshots of how it seamlessly works with [Streamdown's](https://github.com/day50-dev/Streamdown) built in `Savebrace` feature and how it helps workflow.
![2025-04-26_18-45](https://github.com/user-attachments/assets/a81cbcea-cb15-46d9-92ac-5430238b2b85)

![2025-04-26_18-49](https://github.com/user-attachments/assets/c8b98e30-cd09-47bc-b751-02a929a82703)

![2025-04-26_18-49_1](https://github.com/user-attachments/assets/c752f94f-b780-4a8b-b597-1ce62b2bdb78)

Also you don't need `tmux`! Often you'll be doing things and then realize you want the talk party and you're not in tmux.

That's fine! If you use DAY50's [streamdown](https://github.com/day50-dev/Streamdown),  `sc-picker` works like it does inside tmux. You can also `sc-add` by id. It's not great but you're not locked in. That's the point!

## Advanced features

### Amnesia
`/amnesia` is a selective memory feature to fight against context rot. I 

 * Use `/prev` to see the previous conversations
 * Scroll up (or use the fzf fuzzy finder) to find one I want to talk about
 * Use `/amnesia` to get a summary of the conversation
 * This time I use fzf to select the topics I want to carry on to the new context
 * Then a new context is made, the concepts get injected and we're ready to go

https://github.com/user-attachments/assets/03f5e3cb-594b-44a1-a6f1-013ad066bfc6

