#!/bin/bash

# wait for db server to start
while ! mysqladmin ping -h"db" --silent; do
    sleep 1
done

bash /root/cleaner.sh &

apache2-foreground