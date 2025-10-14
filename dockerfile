FROM python:3.13-slim

RUN mkdir -p /app

WORKDIR /app

COPY ./ ./

RUN python -m pip install -r /app/src/requirements.txt --no-cache-dir --upgrade

CMD ["python3", "src/fcc_tool.py", "--update", "--non-interactive"]