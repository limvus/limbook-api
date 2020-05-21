# Limbook Api
![](https://github.com/limvus/limbook-api/workflows/limbook-api-ci/badge.svg)

Limbook api is a minimal api for creating social app like facebook or twitter. 
It has basic features like user, role and permission management plus support 
for posts, comments, react and friends. It is currently at version 1.0. More 
features will be added in the next release, so keep checking for updates.

** For documentation of API visit here: **
 
**[API DOCUMENTATION](https://documenter.getpostman.com/view/3230491/SzmmVueg)**

## Features
- Authentication
- User
- Role
- Permission
- Friend
- Post
- Comment
- React
- Image Manager

** Upcoming Features **
- Chat
- Notification
- Activity
- User Bot

## System Requirements
- Python >= 3.7
- Pip >= 19.0

Note: may run in lower version but haven't tested.

## Technology Used
- Python
- Flask
- Flask-SQlalchemy
- Redis
- Redis Queue
- Postgresql

## Installation
Using virtual environment
```shell script
# go to project directory and create venv
$ virtualenv venv
$ (or) python3 -m venv path_to_project/venv
# source venv from project directory
$ source venv/bin/activate
```
Install dependencies
```shell script
$ pip install -r requirements.txt
```
Export secrets
```shell script
# in ~/.profile add your env variables:
export SECRET_KEY='my_secret_key' #any random string
export DATABASE_URL= #db path
export REDIS_URL= # redis url
export MAIL_SERVER= # mail server host
export MAIL_PORT= # mail server port
export MAIL_USERNAME= # mail username
export MAIL_PASSWORD= # mail password
# logout and login or
$ source ~/.profile
```
Run migration
```shell script
# initialize and run migration
flask db init
flask db migrate
flask db upgrade
```
Seed demo data
```shell script
flask seed run
# Security Note: seed data has some default users with password.
# admin@gmail.com/password
# verified_user@gmail.com/password
# unverified_user@gmail.com/password
```
Run app
```shell script
# using python
python run.py
# using flask
export FLASK_APP=limbook_api
flask run
```

## Test
```shell script
# Simply run pytest from the root directory.
pytest
```

Debugging with python interpreter
```
# in the command line
python

# inside python interpreter set app context
from run import app

# now you can test and try
from limbook_api.setup_db import db
from limbook_api.models import Post
post = Post(user_id="id",content="my post")
db.session.add(post)
```

## Contribution
If you want to contribute, just fork the repository and play around, create 
issues and submit the pull request. Help is always welcomed.

## Security
If you discover any security related issues, please email hello@sudiplimbu.com 
instead of using the issue tracker.

## Author
Sudip Limbu