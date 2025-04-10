#!/bin/bash

# Simple stress test using curl in a loop

URL="http://localhost:30007/"   # Replace with your actual endpoint
TOTAL=250                       # Total number of requests

for ((i=1; i<=TOTAL; i++))
do
  curl -s -o /dev/null "$URL" &
done

wait
echo "Sent $TOTAL requests to $URL"
