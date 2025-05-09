#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIP="$( (which pipx || which pip ) | tail -1 ) install"
[[ $PIP =~ 'pipx' ]] && PIP="$PIP " || PIP="$PIP --break-system-packages"

insdir="$HOME/.local/bin"
set -eEuo pipefail
trap 'echo "Error on line $LINENO"; read -rp "Press enter to exit..."; exit 1' ERR
echo -e "\n  INSTALLING\n"

[[ -d "$insdir" ]] || mkdir -p "$insdir"

touch ~/.tmux.conf
if ! grep -q "bind h run-shell" ~/.tmux.conf; then
cat << ENDL >> ~/.tmux.conf
bind h run-shell "tmux split-window -h '$insdir/screen-query #{pane_id}'"
bind j display-popup -E "$insdir/sq-picker"
ENDL
    if pgrep -u $UID tmux > /dev/null; then
        tmux source-file "$HOME"/.tmux.conf
    fi
fi

for cmd in sq-add sq-picker screen-query; do
    rm -f "$insdir"/$cmd 
    echo "  ✅ $cmd"
    cp -pu "$DIR"/$cmd "$insdir"
done

for pkg in llm streamdown; do
    echo "  ✅ $pkg"
    $PIP $pkg &> /dev/null
done

if [[ ! -d ~/.fzf ]]; then
    echo "  ✅ fzf"
    git clone --quiet --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    ~/.fzf/install
fi
    

if ! echo $PATH | grep "$insdir" > /dev/null; then

    echo "Notice!\nAdd $insdir to your path."
fi
{
cat <<ENDL

### **Success**

You're ready to go.

screen-query's tmux key strokes:

 * **tmux key + h**: Chat window
 * **tmux key + j**: Recent code snippets

You'll need to set up **LLM**:
[https://github.com/simonw/llm](https://github.com/simonw/llm)

Our Recommendation:
 1. \`llm install llm-openrouter\`.
 2. Set up some integration keys.
 3. Use the free models.
ENDL

} | $insdir/sd 
