#!/usr/bin/env bash
git pull
python ./update.py
git config user.name "Server"
git config user.email "ubuntu@localhost"
git add .
git commit -m ":book: update by server"
