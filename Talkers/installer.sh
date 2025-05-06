#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIP=$( (which pipx || which pip ) | tail -1 )
insdir="$HOME/.local/bin"
{
cat <<ENDL

I'm an intentionally stupid installer! It should probably work, but this is no guarantee, not in the slightest. Luckily it's easy to read.

ENDL
} | fold -s
read -p "Continue? "
set -eEuo pipefail
trap 'echo "Error on line $LINENO"; read -rp "Press enter to exit..."; exit 1' ERR
echo

[[ -d "$insdir" ]] || mkdir -p "$insdir"

if ! grep -q "bind h run-shell" ~/.tmux.conf; then
cat << ENDL >> ~/.tmux.conf
bind h run-shell "tmux split-window -h 'screen-query #{pane_id}'"
bind j display-popup -E "sq-picker"
ENDL
    if pgrep tmux; then
        tmux source-file "$HOME"/.tmux.conf
    fi
fi

cd "$insdir"
for cmd in sq-add sq-picker screen-query; do
    [[ -e $cmd ]] && unlink $cmd 
    ln -s "$DIR"/$cmd .
done

for pkg in llm streamdown; do
    $PIP install $pkg
done

if ! echo $PATH | grep "$insdir" > /dev/null; then
    echo "Now add $insdir to your path because I just blindly put things there. See, I told you this was stupid."
fi
{
cat <<ENDL

# **I Think We're Done**

Well that seems to not have crashed.
Here's the key strokes:

 * **tmux key + h** -- chat window
 * **tmux key + j** -- recent code snippets

And that's about it!

Also, there's a few other things you probably need

### fzf
Many package managers are quite a bit behind in the modern features so even if you have it installed, if it seems to break, this is why.
\`\`\`bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
\`\`\`
You can get this now as your last streamdown brace using \`sq-picker 1\`

see here: [https://github.com/junegunn/fzf](https://github.com/junegunn/fzf)

### simonw's llm
You'll need to set this up

See here: [https://github.com/simonw/llm](https://github.com/simonw/llm)

My recommendation is to install the openrouter plug-in, set up some integration keys and you can use a bunch of models for free.
ENDL

} | sd
