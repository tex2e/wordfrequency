#!/bin/bash

tmpfile=`mktemp`
trap "rm $tmpfile" SIGINT

for file in $(find extracted/?? -type f -name '*.token'); do
  cat "$file" | tr 'A-Z' 'a-z' > "$tmpfile"
  mv "$tmpfile" "$file"
done
