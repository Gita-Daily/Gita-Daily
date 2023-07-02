#!/bin/bash
echo "Stopping PM2"
pm2 stop 0
echo "Starting PM2"
pm2 start app.js
echo "PM2 restart complete at $(date)"
