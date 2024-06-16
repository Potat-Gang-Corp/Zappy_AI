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

# Configurer le gestionnaire de signal pour intercepter CTRL+C (SIGINT)
trap cleanup INT

while [ $count -lt $max_processes ]; do
    ./zappy_ai -p 8080 -n e > e.txt &
    pids="$pids $!" 
    count=$((count + 1))
    sleep 0.5 
done

while true; do
    sleep 1
done
