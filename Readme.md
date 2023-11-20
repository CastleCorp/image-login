# Image-Login

A crappy Flask app that uses a username and image to authenticate a user, inspired by a comment on /r/badUIBattles that I can no longer find.

## Setup
Requires python3
Run `pip3 install -r requirements.txt` to install dependencies, then `python3 login.py` to start the server.

## Usage
Just enter a username, select an image for your password, and register your account.
To login, enter your username, upload the same image, and you'll be logged in.

An SQLite database called `users.db` will automatically be setup if it is not already.

## Disclaimer
This is not even remotely close to best practice - it's a joke. Do not implement this anywhere.