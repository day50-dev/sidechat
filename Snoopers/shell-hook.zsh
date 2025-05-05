shell_hook() {
  local QUESTION="$BUFFER"
  local SHELL=$(ps -p $$ -o command= | awk '{print $1}')
  local PROMPT="
  You are an experienced Linux engineer with expertise in all Linux
  commands and their
  functionality across different Linux systems.

  Given a task, generate a single command or a pipeline
  of commands that accomplish the task efficiently.
  This command is to be executed in the current shell, $SHELL.
  For complex tasks or those requiring multiple
  steps, provide a pipeline of commands.
  Ensure all commands are safe and prefer modern ways. For instance,
  homectl instead of adduser, ip instead of ifconfig, systemctl, journalctl, etc.
  Make sure that the command flags used are supported by the binaries
  usually available in the current system or shell.
  If a command is not compatible with the
  system or shell, provide a suitable alternative.

  The system information is: $(uname -a) (generated using: uname -a).
  The user is $USER. Use sudo when necessary

  Create a command to accomplish the following task: $QUESTION

  If there is text enclosed in paranthesis, that's what ought to be changed

  Output only the command as a single line of plain text, with no
  quotes, formatting, or additional commentary. Do not use markdown or any
  other formatting. Do not include the command into a code block.
  Don't include the shell itself (bash, zsh, etc.) in the command.
  "
  local model=''

  if [[ -r "$HOME/.config/io.datasette.llm/default_model.txt" ]]; then
    model=$(< $HOME/.config/io.datasette.llm/default_model.txt)
  fi

  BUFFER="$QUESTION ... $model"
  zle -R
  local response=$(llm "$PROMPT")
  local COMMAND=$(echo "$response" | sed 's/```//g' | tr -d '\n')
  echo "$(date %s) {$QUESTION | $response}" >> /tmp/shell-hook
  if [[ -n "$COMMAND" ]] ; then
      BUFFER="$COMMAND"
      CURSOR=${#BUFFER}
  else
      BUFFER="$QUESTION ... no results"
  fi
}

zle -N shell_hook

bindkey '^Xx' shell_hook

