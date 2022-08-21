# storage_app

This is a repository for a web application developed with Django

## Table of Contents

1. [Project Structure](#project-structure)
2. [Features](#features)
3. [Getting Started: Backend](#getting-started-backend)
   - [Docker Setup (recommended)](#docker-setup-recommended)
   - [Local Setup](#local-setup-alternative-to-docker)
4. [Usage](#usage)
   - [Admin Panel](#admin-panel)
   - [API Documentation](#api-documentation)

## Project Structure

    ..
    ├── home                           # Starter home app
    ├── modules                        # Modules app
    ├── storage_app           # Django project configurations
    ├── static                         # Static assets
    ├── users                          # Starter users app
    ├── web_build                      # React Native Web build
    ├── ...
    ├── README.md
    └── ...

## Features

1. **Local Authentication** using email and password with [allauth](https://pypi.org/project/django-allauth/)
2. **Rest API** using [django rest framework](http://www.django-rest-framework.org/)
3. **Forgot Password**
4. [Bootstrap4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
5. Toast Notification
6. Inline content editor in homepage

# Getting Started: Backend

Following are instructions on setting up your development environment.

The recommended way for running the project locally and for development is using Docker.

It's possible to also run the project without Docker.


## Local Setup (Alternative to Docker)

1. [Postgresql](https://www.postgresql.org/download/)
2. [Python](https://www.python.org/downloads/release/python-365/)

### Installation

1. Install [pipenv](https://pypi.org/project/pipenv/)
2. Clone this repo and `cd storage_app`
3. Run `pip install --user --upgrade pipenv` to get the latest pipenv version.
4. Run `pipenv --python 3.8`
5. Run `pipenv install`
6. Run `cp .env.example .env`
7. Update .env file `DATABASE_URL` with your `database_name`, `database_user`, `database_password`, if you use postgresql.
   Can alternatively set it to `sqlite:////tmp/my-tmp-sqlite.db`, if you want to use sqlite for local development.

### Getting Started

1. Run `pipenv shell`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Run `python manage.py runserver`

# Usage

## Admin Panel

Admin Panel can be accessed through http://localhost:8000/admin/. If you are the Project Owner, admin credentials can be generated from App > 

## API Documentation

API Documentation is generated automatically and can be access through http://localhost:8000/api-docs/. Please make sure you are signed in to the admin panel before navigating to this page.
