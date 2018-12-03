#!/usr/bin/env bash

export FLASK_APP=sigsec
pipenv lock -r > requirements.txt
pip3 install -r requirements.txt
service sigsecweb restart
