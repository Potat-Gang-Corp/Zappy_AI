#!/bin/sh

count=0
max_processes=10
pids=""

cleanup() {
    for pid in $pids; do
        kill $pid 2>/dev/null
    done
    wait
    echo "All processes stopped."
    exit 0
}

trap cleanup INT

while [ $count -lt $max_processes ]; do
    ./zappy_ai -p 8080 -n e > e.txt &
    pids="$pids $!" 
    count=$((count + 1))
    sleep 0.5 
done

wait

echo "All AIs are done"