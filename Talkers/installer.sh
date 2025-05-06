#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
insdir="$HOME/.local/bin"
{
cat <<ENDL

I'm an intentionally stupid installer! We're going to set -x so you can see what I'm doing. It should probably work, but this is no guarantee, not in the slightest. Luckily it's easy to read.

ENDL
} | fold -s
read -p "Continue? "
set -eEuo pipefail
trap 'echo "Error on line $LINENO"; read -rp "Press enter to exit..."; exit 1' ERR
echo
set -x

[[ -d "$insdir" ]] || mkdir -p "$insdir"

if ! grep -q "bind h run-shell" ~/.tmux.conf; then
cat << ENDL >> ~/.tmux.conf
bind h run-shell "tmux split-window -h 'screen-query #{pane_id}'"
bind j display-popup -E "sq-picker"
ENDL
tmux source-file $HOME/.tmux.conf
fi

cd "$insdir"
for cmd in sq-add sq-picker screen-query; do
  [[ -e $cmd ]] || ln -s $DIR/$cmd .
done

pipx install --force streamdown llm

if ! echo $PATH | grep "$insdir" > /dev/null; then
    echo "Now add $insdir to your path because I just blindly put things there. See, I told you this was stupid."
fi
set +x
{
cat <<ENDL

# I Think We're Done

Well that seems to not have crashed.
Here's the key strokes:

 * **tmux key + h** -- chat window
 * **tmux key + j** -- recent code snippets

And that's about it!

Also, there's a few other things you probably need

### fzf
\`\`\`bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
\`\`\`

see here: [https://github.com/junegunn/fzf](https://github.com/junegunn/fzf)

### simonw's llm
You'll need to set this up

See here: [https://github.com/simonw/llm](https://github.com/simonw/llm)

ENDL

} | sd
