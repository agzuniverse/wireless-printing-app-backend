# Wireless Printing App

This is a backend made in Django for the wireless printing app project of FOSSMEC.

The server interfaces with a printer to print documents sent in by authenticated users. A credit system is used to limit the number of pages a user can print.

A task queue implemented with RabbitMQ + Celery is used to make the printing action asynchronous, avoiding conflicts and server freezes.

## Pre-requisites

- Install Python 3.x
- Install virtualenv and pip (Typically is included with the Python installation)
- Install [RabbitMQ](http://www.rabbitmq.com/download.html) (Also typically requires you to install Erlang because RabbitMQ runs on Erlang VM.)

## Setup

- Clone this repo
- Run `virtualenv server`
- Activate the `virtualenv` by running `server/Scripts/activate` (`activate.bat` for Windows users)

* Install requirements with `pip install -r requirements.txt`
* From `backend/`, Run the following commands:

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Enter username and password when promted during superuser creation.

- run `python manage.py runserver` to start the Django server.

* In a new terminal, create a new administrator in RabbitMQ (Use rabbitmqctl.bat in a cmd with administrative permissions for the following steps if you're on Windows.)
  - sudo rabbitmqctl add_user username password
  - sudo rabbitmqctl set_user_tags username administrator
  - sudo rabbitmqctl set_permissions username ".\*" ".\*" ".\*"
  - sudo rabbitmq-plugins enable rabbitmq_management

- Now visit `localhost:15672` in your browser to make sure RabbitMQ is running. (You'll be prompted to log into RabbitMQ dashboard. Login with the user you just created.)

- In a new terminal, `cd` to this project directory and activate `virtualenv`.
- Run `celery -A backend worker -l info` (For Windows users run `celery -A backend --pool=eventlet`)

* That's it!

### TO DO

- Move from SQLite3 to PostgreSQL database
- Add a wrapper function around printing to handle all possible errors and to optimize the process.
