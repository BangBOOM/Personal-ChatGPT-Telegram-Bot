# Personal-ChatGPT-Telegram-Bot


This bot only supports one person using it!!!

## How to run the code

+ Get the token and key then run these two commands

```bash
export TELEGRAM_TOKEN="xxx"
export OPENAI_API_KEY="xxx"
```

+ edit your username in chatbot.py

```python
def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    user_filter = filters.User(username="xxx")
```

+ start the bot

```bash
python chatbot.py
```