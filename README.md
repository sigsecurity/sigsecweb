# SIG-Security Website

## Development Setup

1. Install [pyenv](https://github.com/pyenv/pyenv) for python version management and run `pyenv install 3.7.1`
2. Install [pipenv](https://github.com/pypa/pipenv) for python virtualenv management
3. Clone the repository `git clone git@github.com:trainrex42/sigsecweb.git`
4. Run `pipenv install` to setup your virtual environment
5. Test that the webserver works by running `pipenv run python serve.py` and visiting http://localhost:4523

## Authorization to API

1. Visit `/google/auth` to recieve your authorization URL `auth_url`
2. Navigate to `auth_url` and select your account
3. If `success` = `true` you are now authenticated

## Endpoints

### Authentication

| Route | Methods | Description |
|-------|---------|-------------|
|/google/auth| GET | Get Google OAuth2 URL|
|/google/logout| GET | Logout from the service|

### Users

| Route | Methods | Description |
|-------|---------|-------------|
|`/v1/users`| GET | Retrieve a list of all users|
|`/v1/users/current-user` | GET | Retrieve information about the current user|
|`/v1/users/<int:user_id>`| GET | Get information about a specific user |
|`/v1/users/<int:user_id>`| DELETE | Delete the specified user|

