#!/bin/bash

# wait for db server to start
while ! mysqladmin ping -h"db" --silent; do
    sleep 1
done



#while true; do
	#/service/cleanup.sh
	#sleep 60
#done &
apache2-foreground