#!/bin/bash

# Use environment variable or default to 3 AM on Friday
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 3 * * 5"}
echo "Schedule: $CRON_SCHEDULE"

# Redirect cron output to Docker stdout/stderr
echo "$CRON_SCHEDULE bash /app/run.sh > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/cron.d/python-cron
echo "" >> /etc/cron.d/python-cron

chmod 0644 /etc/cron.d/python-cron
crontab /etc/cron.d/python-cron

# Run once on startup
bash /app/run.sh

# Start cron in foreground
cron -f