#!/bin/bash

echo "Starting init-postgres-pif.py script at $(date +"%Y-%m-%d %H:%M:%S")"
python /app/init-postgres-pif.py
echo "Finished init-postgres-pif.py script at $(date +"%Y-%m-%d %H:%M:%S")"

echo "Starting insert-poem.py script at $(date +"%Y-%m-%d %H:%M:%S")"
python /app/insert-poem.py
echo "Finished insert-poem.py script at $(date +"%Y-%m-%d %H:%M:%S")"

