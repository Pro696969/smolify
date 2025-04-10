#!/bin/bash

BASE_URL="http://localhost:30007"
OUTFILE="results.txt"
TOTAL=50  # Number of requests

> "$OUTFILE"  # Clear previous contents

for ((i=1; i<=TOTAL; i++)); do
  URL_TO_SHORTEN="https://example${i}.com"
  result=$(curl -s -X POST "$BASE_URL" -d "url=${URL_TO_SHORTEN}" | grep -o 'value="https://tinyurl.com/[^"]*"' | sed 's/value="//;s/"$//')
  echo "$result" >> "$OUTFILE"
done

echo "Finished sending $TOTAL requests with unique URLs. Output saved to $OUTFILE"
