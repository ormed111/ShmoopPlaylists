#!/bin/bash

cd $(dirname $0)

export $(cat creds.env | tr -d '\r' | xargs)

# Run backend 
echo "Running backend"
python3 ./backend/main.py &
echo

# Run frontend
cd ./frontend
echo "Running frontend"
yarn serve &

# Open app on web browser (assuming backend port in 1312)
echo "Go to http://localhost:1312/"


# pkill -9 python
# pkill -9 -f "ShmoopPlaylists"
