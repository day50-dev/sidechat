#!/bin/bash
cat << ENDL
      ____  ___   _     ____________
     / __ \/   | ( )  _/_/ ____/ __ \\ 
    / / / / /| |  V _/_//___ \/ / / /
   / /_/ / ___ |  _/_/ ____/ / /_/ /
  /_____/_/  |_| /_/  /_____/\____/

      Keeping AI Productive 
    50 Days In And Beyond
                                                                          
ENDL
insdir=$(mktemp -u)
git clone --quiet https://github.com/day50-dev/sidechat $insdir
$insdir/install.sh
rm -r $insdir
