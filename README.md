<div align="center">
<h1>Task Manager</h1>

<p>
    A simple and flexible task management web application.
</p>

### Hexlet tests and linter status:
[![Actions Status](https://github.com/shizomanya/python-project-lvl4/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/shizomanya/python-project-lvl4/actions)
[![Python CI](https://github.com/shizomanya/python-project-lvl4/actions/workflows/ci.yml/badge.svg)](https://github.com/shizomanya/python-project-lvl4/actions/workflows/ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/b1461bbe9c019ff68bd1/maintainability)](https://codeclimate.com/github/shizomanya/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b1461bbe9c019ff68bd1/test_coverage)](https://codeclimate.com/github/shizomanya/python-project-lvl4/test_coverage)

<p>
<a href="#about">About</a> •
<a href="#installation">Installation</a> •
<a href="#usage">Usage</a> 
</p>
</div>

<details><summary style="font-size:larger;"><b>Table of Contents</b></summary>

- [TASK MANAGER](#task-manager)
  - [About:](#about)
  - [Requirements:](#requirements)
    - [Makefile commands:](#makefile-commands)
  - [Installation:](#installation)
      - [Python](#python)
      - [Poetry](#poetry)
      - [PostgreSQL](#postgresql)
    - [Application](#application)
  - [Usage](#usage)
  - [How to use this App:](#how-to-use-this-app)

</details>

# TASK MANAGER
## About:
[Task Manager](https://python-project-lvl4-k898.onrender.com) is a web application tweb application built with Python and [Django](https://www.djangoproject.com/) framework. The application allows a registered user to create, edit and delete tasks, as well as add an executor, status and labels to them.

## Requirements:
App developed with:
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap 5](https://getbootstrap.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Psycopg 2](https://www.psycopg.org/)
* [Gunicorn](https://gunicorn.org/)
* [Rollbar](https://rollbar.com/)
* [Poetry](https://python-poetry.org/)
* [pytest](https://docs.pytest.org/en/7.2.x/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

### Makefile commands:
Install all dependencies of the package: ```make install```

Install poetry project and start postgresql server: ```make build```

Generate and apply database migrations:  ```make migrate```

Run Django development server at http://127.0.0.1:8000/: ```make dev```

Start gunicorn server: ```make start```

## Installation:

#### Python

Before installing the package make sure you have Python version 3.10 or higher installed:

```bash
>> python --version
Python 3.10.12
```

#### Poetry

The project uses the Poetry dependency manager. To install Poetry use its [official instruction](https://python-poetry.org/docs/#installation).

#### PostgreSQL

As database the PostgreSQL database system is being used. You need to install it first. You can download the ready-to-use package from [official website](https://www.postgresql.org/download/) or use Homebrew:
```shell
>> pip install postgresql
```
### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
>> git clone https://github.com/shizomanya/python-project-lvl4.git && cd python-project-lvl4
```

Then you have to install all necessary dependencies:

```bash
>> make install
```

Create .env file in the root folder and add following variables:
```
DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY = '{your secret key}'
DEBUG = True
ALLOWED_HOSTS = webserver
```
To create the necessary tables in the database, start the migration process:

```bash
>> make migrate
```
---
## Usage

Start the gunicorn Web-server by running:
```bash
make start
```
By default, the server will be available at http://0.0.0.0:8000. 

_It is also possible to start it local in development mode with debugger active using:_
```bash
make dev
```
_The dev server will be at http://127.0.0.1:5000._

## How to use this App:
1. **Registration** — First, you need to register in the application using the registration form provided;
2. **Authentication** — To view the list of tasks and create new ones, you need to log in using the information from the registration form;
3. **Users** — You can see the list of all registered users on the corresponding page. It is available without authorization. You can change or delete information only about yourself. If a user is the author or performer of a task, it cannot be deleted;
4. **Statuses** — You can view, add, update, and delete task statuses if you are logged in. Statuses corresponding to any tasks cannot be deleted;
5. **Tasks** — You can view, add, and update tasks if you are logged in. Only the task creator can delete tasks. You can also filter tasks on the corresponding page with specified statuses, performers, and labels;
6. **Labels** — You can view, add, update, and delete task labels if you are logged in. Labels matching any tasks cannot be deleted.