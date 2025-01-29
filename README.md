# GymBot

**GymBot** is a Telegram bot that helps you in the gym by providing the workout plan for the specific day you need to train. The bot is designed to offer personalized workout routines, track your progress, and help keep you motivated.

## Key Features

- **Personalized workout plans**: GymBot provides you with a daily workout plan based on the program you've set up.
- **User management**: Each user has their own workout plan, stored in a Firebase database.
- **Telegram integration**: Easily interact with GymBot via Telegram, receiving workout plans directly in the chat.

## Requirements

- Python 3.x
- A Telegram account and a bot created through the BotFather on Telegram.
- Firebase database for storing user workout plans.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/crookeDog/GymBot.git
   cd GymBot
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the credentials**:
   - **Telegram Bot Token**: Obtain a token by creating a new bot via BotFather on Telegram.
   - **Firebase Credentials**: If the bot uses Firebase, make sure you have the JSON credentials file.
   - Rename your credentials file as `my_credentials.json` and place it in the root directory.

4. **Run the bot**:
   ```bash
   python main.py
   ```

## Bot Notes

Before starting the bot, change the usernames inserted in the bot's whitelist and create the respective nodes in the Firebase database.

## How to use

After pressing the start button, you can:
- View your workout plan by selecting a day (`A`, `B`, `C`).
- Modify your workout plan by selecting a day and inputting new exercises.
- Check your current training week and either reset or advance it.

## Firebase Database Structure

```plaintext
utenti/
  username/
    a: "Workout Plan Day A"
    b: "Workout Plan Day B"
    c: "Workout Plan Day C"
    settimana: 1
```


   

   


