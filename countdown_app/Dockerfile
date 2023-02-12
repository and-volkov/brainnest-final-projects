FROM python:3.11.1-slim

WORKDIR /app

RUN apt update && apt upgrade -y

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

ENV PYTHONPATH .

COPY ./ .

CMD ["bash"]
