#!/bin/bash

directory="/app/uploads"

while true; do

    find "$directory" -mindepth 1 -maxdepth 1 -mmin +10 -print | while IFS= read -r item; do
        echo "Deleting $item"
        rm -r "$item"
    done
    sleep 60
done
