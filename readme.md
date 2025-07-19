# Telegram Gym Bot

A simple Telegram bot for managing personalized gym workout plans.

## Features

- View and edit daily workout plans (A/B/C days)
- View and update the current training week
- Reset the weekly progress
- Support for Firebase as backend

## Requirements

- Python 3.10+
- Telegram Bot Token
- Firebase service account JSON

## Setup

1. Clone the repo or upload your files.
2. Create a `requirements.txt` file (already included).
3. Replace `YOUR_TOKEN_HERE` in `bot.py` with your actual Telegram Bot token.
4. Upload your Firebase admin SDK JSON and configure `Firebase.py`.

## Run locally

```bash
pip install -r requirements.txt
python bot.py
