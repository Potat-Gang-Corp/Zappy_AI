#!/bin/sh

count=0
max_processes=20
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
    ./zappy_ai -p 12345 -n name1 > e$count.txt &
    pids="$pids $!" 
    count=$((count + 1))
    ./zappy_ai -p 12345 -n name2 > e$count.txt &
    pids="$pids $!" 
    count=$((count + 1))
    sleep 0.4
done

wait

echo "All AIs are done"