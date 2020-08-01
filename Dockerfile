FROM python:3.7-slim-buster

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY src
COPY bot.py

WORKDIR /app
CMD ["python3", "bot.py"]