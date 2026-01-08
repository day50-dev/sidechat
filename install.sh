#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/sidechat
PIP=$(command -v pipx || command -v pip || command -v pip3 )
pybin=
if [[ -z "$PIP" ]]; then 
    echo "Woops, we need python and either pip or pipx."
    exit 1
fi
if ! command -v unzip > /dev/null; then
    echo "Woops, unzip needs to be installed."
fi

if [[ $PIP =~ /pipx$ ]]; then 
    PIP="$PIP install"
    pybin=$(pipx environment 2> /dev/null | grep PIPX_BIN_DIR=/ | cut -d = -f 2)
    # really old pipx - apps is used even in the intl tests i did
    if [[ -z "$pybin" ]]; then
        pybin=$(pipx --help | grep apps | awk ' { print $NF } ' | grep \/ | sed 's/\.$//g;')
    fi
else
    PIP="$PIP install --user"
    if [[ $(uname) == "Linux" || "$(pip3 --version | grep homebrew | wc -l)" != 0 ]]; then
        PIP="$PIP --break-system-packages "
    fi
fi

if [[ $(uname) == "Linux" ]]; then
    insdir="$HOME/.local/bin"
    sd="$insdir/sd"
else
    insdir="$HOME/Library/bin"
    if [[ -z "$pybin" ]]; then 
      pybin=$(python3 -msite --user-base)"/bin"
    fi
    sd="$pybin/sd"
fi

set -eEuo pipefail
trap 'echo "Error on line $LINENO"; read -rp "Press enter to exit..."; exit 1' ERR
echo -e "\n  INSTALLING\n"

[[ -d "$insdir" ]] || mkdir -p "$insdir"

touch ~/.tmux.conf
if ! grep -q "bind h run-shell" ~/.tmux.conf; then
cat << ENDL >> ~/.tmux.conf
bind h run-shell "tmux split-window -h '$insdir/sidechat #{pane_id}'"
bind j display-popup -E "$insdir/sc-picker"
ENDL
    if pgrep -u $UID tmux > /dev/null; then
        tmux source-file "$HOME"/.tmux.conf
    fi
fi

for cmd in simple-parse.py sc-add sc-picker sidechat; do
    rm -f "$insdir"/$cmd 
    echo "  ✅ $cmd"
    cp -p "$DIR"/$cmd "$insdir"
done

for pkg in llm streamdown; do
    echo "  ✅ $pkg"
    $PIP $pkg &> /dev/null
done

if [[ ! -d ~/.fzf ]]; then
    git clone --quiet --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    ~/.fzf/install --no-update-rc --no-completion --no-key-bindings >& /dev/null
    for i in ~/.fzf/bin/*; do
        cmd=$(basename $i)
        rm -f "$insdir"/$cmd
        ln -s "$i" "$insdir"/$cmd 
    done
    echo "  ✅ fzf"
fi

if ! command -v sqlite3 &> /dev/null; then
    command -v wget > /dev/null && wget -q https://www.sqlite.org/2025/sqlite-tools-linux-x64-3490200.zip -O /tmp/sqlite-tools-linux-x64-3490200.zip ||  curl -s https://www.sqlite.org/2025/sqlite-tools-linux-x64-3490200.zip > /tmp/sqlite-tools-linux-x64-3490200.zip
    cd $insdir && unzip -o -q /tmp/sqlite-tools-linux-x64-3490200.zip 
fi
echo "  ✅ sqlite3"

msg="You're ready to go!"

if [[ "$insdir" != "$pybin" ]]; then
    binpath="$insdir:$pybin"
else
    binpath="$insdir"
fi

if [[ $(uname) == "Darwin" ]]; then
    sed -i "" "s^#@@INJECTPATH^PATH=\$PATH:$binpath^g" $insdir/sidechat
    sed -i "" "s^@@VERSION^$(cd $DIR;git describe)^g" $insdir/sidechat
else
    sed -i "s^@@VERSION^$(cd $DIR;git describe)^g" $insdir/sidechat
fi

if ! echo $PATH | grep "$binpath" > /dev/null; then
    if [[ $(uname) == "Linux" ]]; then
        shell=$(getent passwd $(whoami) | awk -F / '{print $NF}')
    else
        shell=$(basename $SHELL)
    fi
    msg="**Important!**"
    if [[ $shell == "bash" ]]; then
        echo "export PATH=\$PATH:$binpath" >> $HOME/.bashrc
        msg="$msg Run \`source ~/.bashrc\`"
    elif [[ $shell == "zsh" ]]; then
        echo "export PATH=\$PATH:$binpath" >> $HOME/.zshrc
        msg="$msg Run \`source ~/.zshrc\`"
    elif [[ $shell == "fish" ]]; then
        config_dir="${XDG_CONFIG_HOME:-$HOME/.config}"
        mkdir -p "$config_dir/fish"
        echo "fish_add_path $binpath" >> "$config_dir/fish"/config.fish
        msg="$msg Run \`source ~/.config/fish/config.fish\`"
    else
        msg="$msg Add $binpath to your path"
    fi
    msg="$msg or restart your shell."
fi
{
cat <<ENDL

### **Success**

$msg

Sidechat's TMUX key strokes:

 * **tmux key + h**: Chat window
 * **tmux key + j**: Recent code snippets

You'll need to set up **LLM**:
[https://github.com/simonw/llm](https://github.com/simonw/llm)

Our Recommendation:
 1. \`llm install llm-openrouter\`.
 2. Set up some integration keys.
 3. Use the free models.
ENDL

} | $sd 
