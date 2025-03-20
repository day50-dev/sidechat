#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Capturing!" | dzen2 -ta c -y 0 -x 0 -p 20 -m -fg "#FEAEAE" -bg "#900000" &
pid1="$!"
question="$(./kb-capture.py)  "
kill $pid1

echo "$question" | dzen2 -ta c -y 0 -x 0 -p 10 -m -fg "#FEAEAE" -bg "#410141" &
pid1="$!"
res=$(llm -xs "Answer this question as briefly as possible" "$question")
kill $pid1
echo "$res" | dzen2 -ta c -y 0 -x 0 -p 1 -m -bg "#FEAEAE" -fg "#110111"

for i in $(seq 0 "${#question}"); do
    xdotool key BackSpace
done

xdotool type "$res"
