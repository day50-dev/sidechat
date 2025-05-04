#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "I'm an intentionally stupid installer! We're going to set -x so you can see the stupid thing it's doing."
echo "It should probably work, but this is no guarantee, not in the slightest. Luckily it's easy to read"
read -p "continue? "
set -x

[[ -d $HOME/bin ]] || mkdir $HOME/bin

if ! grep -q "bind h run-shell" ~/.tmux.conf; then
cat << ENDL >> ~/.tmux.conf
bind h run-shell "tmux split-window -h 'screen-query #{pane_id}'"
bind j display-popup -E "sd-picker"
ENDL
fi

cd $HOME/bin
for cmd in sqa sd-picker screen-query; do
  ln -s $DIR/$cmd .
done

pipx install --force streamdown

set +x
echo "Now add $HOME/bin to your path because I just blindly put things there. See, I told you this was stupid."
