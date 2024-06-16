#!/bin/sh

count=0
max_processes=10
pids=""

# Fonction pour tuer tous les processus en arrière-plan
cleanup() {
    echo "Stopping all processes..."
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
    ./zappy_ai -p 8080 -n f > f.txt &
    pids="$pids $!"  # Collecter les PID des processus en arrière-plan
    count=$((count + 1))
    sleep 0.5  # Ajout d'une pause pour éviter de lancer trop d'instances en trop peu de temps
done

# Attendre indéfiniment jusqu'à ce que l'utilisateur appuie sur CTRL+C
while true; do
    sleep 1
done
