#!/bin/sh
# Create or update the shared labels (labels.tsv) in every repo of the org, or in the repos given as arguments.
# usage: tools/sync-labels.sh [repo ...]      (needs gh, logged in with admin on lepetitatelier)
# New repos also get them automatically the first time an issue or pull request is opened (triage workflow).
set -e
cd "$(dirname "$0")/.."
repos="$*"
[ -n "$repos" ] || repos=$(gh repo list lepetitatelier --limit 200 --no-archived --json name --jq '.[].name')
for r in $repos; do
  while IFS="$(printf '\t')" read -r name color desc; do
    gh label create "$name" --repo "lepetitatelier/$r" --color "$color" --description "$desc" --force >/dev/null
  done < labels.tsv
  echo "labels: $r"
done
