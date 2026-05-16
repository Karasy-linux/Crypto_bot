# Crypto_bot

A lightweight and robust Telegram bot designed to monitor real-time cryptocurrency price changes and notify users about price deltas.

## Features

- **Automated Monitoring:** Fetches cryptocurrency prices from the CoinGecko API every 10 minutes.
- **Price Delta Calculation:** Automatically calculates percentage changes between old and new prices.
- **Robust Error Handling:** Properly handles API timeouts and SQLite database locks without crashing.
- **Clean Architecture:** Built with Python 3.12, SQLite, and pyTelegramBotAPI.

## Tech Stack

- **Language:** Python 3.12
- **Database:** SQLite
- **OS Environment:** Debian 13 (Trixie) with systemd service deployment

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Karasy-linux/Crypto_bot.git](https://github.com/Karasy-linux/Crypto_bot.git)
   cd Crypto_bot

Install dependencies:
Bash

```pip install -r requirements.txt```

Configure Environment Variables:
Create a .env file or export your API tokens:
Bash
```
export API_KEY="your_coingecko_api_key"
export BOT_TOKEN="your_telegram_bot_token"
```
Run the application:
Bash

python main.py