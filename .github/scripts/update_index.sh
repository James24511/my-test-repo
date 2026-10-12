#!/bin/bash
# Updates index.html with the task lists and unit test results.
#   $1 = file containing the output of todo.py
#   $2 = file containing the output of todo-test.py

HTML_FILE="index.html"

# Extract tasks and test data and store them in local variables
TODO_TASKS=$(grep -A 1000 "ToDo Tasks:" "$1" | sed '1d; /Done Tasks:/,$d' | sed '/^[[:space:]]*$/d')
DONE_TASKS=$(awk '/Done Tasks:/,/^[[:space:]]*$/ { if (NR>1 && !/Done Tasks:/) print }' "$1")
UNIT_TEST_RESULTS=$(cat "$2")

# Function to replace the content of <pre id="..."> in the HTML file
update_pre() {
  perl -i -0777 -pe "s{<pre id=\"$1\">.*?</pre>}{<pre id=\"$1\">\n$2\n</pre>}gs" "$3"
}

update_pre "pending"   "$TODO_TASKS"        "$HTML_FILE"
update_pre "completed" "$DONE_TASKS"        "$HTML_FILE"
update_pre "unittest"  "$UNIT_TEST_RESULTS" "$HTML_FILE"

# Commit and push the updated index.html back to the repository
git config --global --add safe.directory "$(pwd)"
git config --global user.email "github-actions@users.noreply.github.com"
git config --global user.name "github-actions[bot]"
git add "$HTML_FILE"
git commit -m "Update $HTML_FILE with new task and test data (run by ${GITHUB_USER:-unknown})" \
  || echo "No changes to commit"
# Pick up anything pushed to main while this pipeline was running, then push
#   --autostash : ignore local leftovers (e.g. the chmod done in the Dockerfile)
#   -X theirs   : if index.html changed meanwhile, keep this run's version
git pull --rebase --autostash -X theirs origin main
git push origin HEAD:main
