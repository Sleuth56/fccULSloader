#!/bin/bash

# Use environment variable or default to 3 AM on Friday
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 3 * * 5"}

# Create cron job with the schedule from environment variable
echo "$CRON_SCHEDULE /app/run.sh" > /etc/cron.d/python-cron
chmod 0644 /etc/cron.d/python-cron
crontab /etc/cron.d/python-cron

# Start cron and tail the log
cron && tail -f /var/log/cron.log

bash /app/run.sh