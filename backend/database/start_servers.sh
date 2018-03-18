#!/bin/bash
node ./start_deepstream.js &
sleep 5
node ./start_deepstream-search.js &

