#!/bin/bash
if [[ ! "$(getent passwd $(whoami) | cut -d: -f7)" =~ zsh ]]; then
    echo "oh brother, we are kind of a zsh house here ... let's see what we can do."
fi
cat << END
You can do this. Just do:

cat shell-hook.zsh wtf >> .zshrc

The zsh part of shell-hook is how it binds. Totally fixable for all the others!
END
