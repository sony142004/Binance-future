# Binance Futures Testnet Trading Bot

A simplified Python trading bot for placing orders on the Binance Futures Testnet (USDT-M). This bot uses direct REST calls via the `requests` library.

## Features

- Place **MARKET** and **LIMIT** orders.
- Support for **BUY** and **SELL** sides.
- Clean CLI interface with clear input validation.
- Extensive logging to both console and `logs/trading_bot.log`.
- Robust error handling for network inputs and API errors.
- Enhanced CLI styling using `rich`.

## Directory Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance testnet API client
│   ├── orders.py          # Order placement logic
│   ├── logging_config.py  # Logger setup
│   └── validators.py      # Input validation logic
│
├── cli.py                 # CLI entry point
├── .env.example           # Example environment variables
├── requirements.txt       # Dependencies
└── README.md              # Setup and execution guide
```

## Setup Instructions

### 1. Prerequisites
- Python 3.7+ installed.
- Valid API Keys for Binance Futures Testnet. You can obtain these by logging into the [Binance Futures Testnet](https://testnet.binancefuture.com/) with a GitHub account and generating API keys.

### 2. Check out the project
Ensure you are in the `trading_bot` directory.

### 3. Install Dependencies
It's recommended to create a virtual environment first:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install the requirements:
```bash
pip install -r requirements.txt
```

### 4. Configuration
1. Copy the example `.env` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and insert your Testnet API Key and Secret:
   ```
   BINANCE_API_KEY=your_actual_api_key_here
   BINANCE_API_SECRET=your_actual_api_secret_here
   ```

## How to Run Examples

Use the `cli.py` script to run the bot. It requires specific arguments for symbol, side, type, quantity, and price (if LIMIT).

### Example 1: Place a MARKET BUY Order
This will buy 0.001 BTC at the current market price.
```bash
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.001
```

### Example 2: Place a LIMIT SELL Order
This will place a sell order for 0.001 BTC if the price reaches 90000.
```bash
python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.001 --price 90000
```

### Get CLI Help
You can see all available options by running:
```bash
python cli.py --help
```

## Logs
All API interactions and internal events are logged in the `logs/trading_bot.log` file, which is created automatically upon first run.

## Assumptions
- Uses Binance Futures Testnet (`https://testnet.binancefuture.com`). Do not use real funds.
- Time in force for limit orders defaults to "GTC" (Good Till Canceled).
- Logging is stored locally in the `logs/` directory.

## Testing
Logs are attached as part of the submission to verify the successful placement of at least one MARKET order and one LIMIT order.
