#!/usr/bin/env bash
# This is an OS X install-time hack
#@@INJECTPATH

VERSION="@@VERSION"

tmp="$(python3 -c "import tempfile;print(tempfile.gettempdir())")"

[[ "$(uname)" == "Darwin" ]] && \
    CONFIG="Library/Application Support" ||\
    CONFIG=".config"
CONFIG="${HOME}/${CONFIG}/sidechat"
SETTINGS="$CONFIG/settings"
[[ -e "$SETTINGS" ]] && source "$SETTINGS"

[[ -r "$CONFIG" ]] || mkdir -p "$CONFIG"
MDIR="$tmp"/sidechat
[[ -d "$MDIR" ]] || (mkdir "$MDIR" && chmod 0777 "$MDIR")
MDIR="$MDIR/$UID"
[[ -d "$MDIR" ]] || mkdir "$MDIR"
MDREAD='sd -c <(echo -e "[style]\nMargin = 4")'
