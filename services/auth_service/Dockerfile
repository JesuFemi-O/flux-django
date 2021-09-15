FROM python:3.9

ENV pythonunbuffered=1

COPY src app/

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "./run.sh"]