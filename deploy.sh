#!/usr/bin/env bash

export FLASK_APP=sigsec
pipenvtorequirements Pipfile.lock > requirements.txt
pip3 install -r requirements.txt
flask db upgrade
service sigsecweb restart
