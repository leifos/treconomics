git status | grep "mod" 
git status | grep "mod" | grep -v ".DS" | awk '{printf "%s ", $2  } END {print ""}'
