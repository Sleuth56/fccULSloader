FROM python:3.13-slim

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./ ./

RUN python -m pip install -r /app/src/requirements.txt --no-cache-dir --upgrade

RUN ln -s /app/src/data /data

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/run.sh

# Create log file
RUN touch /var/log/cron.log

CMD ["bash", "/app/entrypoint.sh"]