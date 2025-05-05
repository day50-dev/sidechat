function wtf {
  local -a files
  while IFS= read -r i; do
    files+=("$i")
  done

  local width=$(( ( $(tput cols) * 4 ) / 5))
  local head=$(( width / 2 ))
  local question="$1"
  local each_question
  local first=
  local lines=50

  [[ -n "$question" ]] && each_question="Lastly, $question ONLY If this file is relevant to the question, tell me in bold after the summary. If not relevant, do not refer to this question and do not answer this question."

  for i in "${files[@]}"; do
    if [[ -f "$i" && "$(mimetype "$i" | grep text | wc -l)" -gt 0 ]]; then
      date=$(git log -1 --format="%ad" --date=short -- "$i" 2> /dev/null )
      desc=$( head -$lines $i | iconv -f UTF-8 -t ASCII//TRANSLIT | llm $first "I've included the first $lines lines of '$i'. Briefly summarize it. Do not be conversational. Do not include code. Your response will be a command outpuat. DO NOT include the file name. Again, DO NOT INCLUDE THE FILE NAME. Make sure your output does not have code. $each_question")
      printf "%-${head}s $date\n" $i
      echo "$desc" | sd
      echo
      [[ -z "$first" ]] && first="-c"
    fi
  done

  printf '\xe2\x80\x95%.0s' $(seq 1 $(tput cols))
  [[ -n "$question" ]] && last_question="Finally, list the top 4 scripts or code files that are relevant to the question '$question'."
  llm -c "Finally, summarize and cluster files based on their descriptions into an outline form (${files[*]}). Cluster them together and break it into categories. Put the most important things first. Don't be conversational. $last_question" | sd
}

