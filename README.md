# DjangoChat

## Description
Simple single room, chat server. Powered by Django, RabbitMQ and Redis.

## Instalation
Requirements:
 - [Ubuntu 17.10](https://www.ubuntu.com/desktop)
 - [Docker](https://docs.docker.com/)
 - [RabbitMQ](https://www.rabbitmq.com/getstarted.html)
 - [Python 3.7 +](https://www.python.org/)

### Installing system dependencies
We need to install Docker and RabbitMQ.
```
$ sudo apt-get install rabbitmq-server
$ sudo apt-get install docker
$ sudo service rabbitmq-server start
$ sudo docker run -p 6379:6379 -d redis:2.8
```

### Creating virtual environment
This guide uses virtualenvwrapper. For more information please check this [link](https://virtualenvwrapper.readthedocs.io/en/latest/).
```
$ mkvirtualenv djangochat
$ workon djangochat
```

### Cloning repository and installing python3 dependencies
For more information regarding python3 dependencies please refer to requirements.txt file.
```
$ (djangochat) git clone https://github.com/hernannieto89/djangochat
$ (djangochat) cd djangochat
$ (djangochat) pip3 install -r requirements.txt
```

### Executing RabbitMQ listener bot
This script needs to be executed on a separated tab.
```
$ (djangochat) cd rabbitmq
$ (djangochat) python listener.py
```

### Executing django server
It is strongly recommended to create a superuser for django administrator.
```
$ (djangochat) python manage.py makemigrations
$ (djangochat) python manage.py migrate
$ (djangochat) python manage.py createsuperuser
$ (djangochat) python manage.py runserver
```

## Usage
After running django's runserver directive:
```
Performing system checks...

System check identified no issues (0 silenced).
October 21, 2018 - 04:37:00
Django version 2.1.2, using settings 'djangochat.settings'
Starting ASGI/Channels version 2.1.3 development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
2018-10-21 04:37:00,958 - INFO - server - HTTP/2 support not enabled (install the http2 and tls Twisted extras)
2018-10-21 04:37:00,958 - INFO - server - Configuring endpoint tcp:port=8000:interface=127.0.0.1
2018-10-21 04:37:00,959 - INFO - server - Listening on TCP address 127.0.0.1:8000
```
Development server is available at http://127.0.0.1:8000/.

#### Index
Located at localhost:port/, the index page redirects to login if need.
The chat room is available once the user has logged in.
[PIC 1](https://github.com/hernannieto89/djangochat/tree/master/readme_utils/chatroom1.png)
[PIC 2](https://github.com/hernannieto89/djangochat/tree/master/readme_utils/chatroom2.png)

#### Login
Login page, located at localhost:port/login
[PIC 1](https://github.com/hernannieto89/djangochat/tree/master/readme_utils/login.png)

#### Signup
Signup page, located at localhost:port/register
[PIC 1](https://github.com/hernannieto89/djangochat/tree/master/readme_utils/register.png)

#### Profile
User profile page, located at localhost:port/profile.
Immediately after signing up, an empty profile is created.
This page allows the user to update its profile.
[PIC 1](https://github.com/hernannieto89/djangochat/tree/master/readme_utils/logout.png)

#### Logout
Logout page, located at localhost:port/logout.

#### Bot
Currently the bot handles only one command '/stock=STOCK_NAME'.
This command gets stock price information and post it on the chat room.
This is an example of listener.py console output:
```
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received b'/stock=AAPL'
Sent: AAPL quote is $219.31 per share
 [x] Received b'/stock='
Sent: Parameter missing.
 [x] Received b'/wrong_cmd=1'
Sent: Invalid command.
```