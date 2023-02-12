## Countdown CLI App

This is a simple CLI app that counts down from a given number of seconds.

### Technologies
* Python 3.11.1
* Docker 20.10.21
* Textual 0.10.1

### Usage

#### Local command line
From the root directory of the project, run the following commands:
```
pip install --upgrade pip
```
```
pip install -r requirements.txt
```
```
python countdown.py
```

#### Docker
From the root directory of the project, run the following commands:
```
docker build -t countdown_app .
```
Running container in detached mode
```
docker run -dit --name countdown_app --rm countdown_app
```
Start application in container
```
docker exec -it countdown_app python3 countdown.py
```

### Usage
When app is running, you have the following options:
* A - add a new countdown
* R - remove a countdown
* I - set a new interval for last added countdown
* D - toggle dark mode