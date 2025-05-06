#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
insdir="$HOME/.local/bin"
echo "I'm an intentionally stupid installer! We're going to set -x so you can see what I'm doing"
echo "It should probably work, but this is no guarantee, not in the slightest. Luckily it's easy to read"
read -p "continue? "
set -x

[[ -d "$insidr" ]] || mkdir -p "$insdir"

if ! grep -q "bind h run-shell" ~/.tmux.conf; then
cat << ENDL >> ~/.tmux.conf
bind h run-shell "tmux split-window -h 'screen-query #{pane_id}'"
bind j display-popup -E "sq-picker"
ENDL
fi

cd "$insdir"
for cmd in sq-add sq-picker screen-query; do
  ln -s $DIR/$cmd .
done

pipx install --force streamdown

if ! echo $PATH | grep "$insdir" > /dev/null; then
    echo "Now add $insdir to your path because I just blindly put things there. See, I told you this was stupid."
fi
set +x
