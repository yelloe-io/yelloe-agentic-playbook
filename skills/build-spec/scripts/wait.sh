#!/usr/bin/env bash
set -euo pipefail

prefix=refs/remotes
if [ "${1:-}" = "-r" ]; then
  prefix=$2
  shift 2
fi

state() {
  git for-each-ref --format='%(refname) %(objectname)' "$prefix"
  for file in "$@"; do
    if [ -e "$file" ]; then
      echo "$file $(cksum < "$file")"
    else
      echo "$file missing"
    fi
  done
}

before=$(state "$@")
end=$((SECONDS + 150))
while [ "$SECONDS" -lt "$end" ]; do
  sleep 5
  after=$(state "$@")
  if [ "$after" != "$before" ]; then
    diff <(echo "$before") <(echo "$after") | grep '^>' || true
    exit 0
  fi
done
echo "no change"
