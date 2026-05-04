# Plaid Explorer

A Python command-line application that connects to the Plaid financial API sandbox 
to retrieve, analyze, and report on account and transaction data. Built as a learning 
project to demonstrate real-world API integration patterns including authentication 
flows, data retrieval, error handling, and webhook processing.

## Prerequisites

- Python 3.10+
- A free Plaid sandbox account at dashboard.plaid.com
- Your Plaid client_id and sandbox secret

## Setup

1. Clone the repository:
   git clone https://github.com/lfulk33/plaid-explorer.git
   cd plaid-explorer

2. Create and activate a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create a .env file in the project root:
   PLAID_CLIENT_ID=your_client_id_here
   PLAID_SECRET=your_sandbox_secret_here
   PLAID_ENV=sandbox

## How to Run

Run with defaults (30 days back, 10 transactions):
   python3 main.py

Specify days and transaction limit:
   python3 main.py --days 7 --limit 5

Generate and save a report file:
   python3 main.py --days 30 --save

Run the webhook receiver:
   python3 webhook.py
   # Listens at http://localhost:5000/webhook

## Project Structure

main.py         — Entry point, CLI argument handling, output orchestration
auth.py         — Plaid client setup, token exchange flow
accounts.py     — Account data retrieval and health analysis
transactions.py — Transaction retrieval and spend analysis
webhook.py      — Flask webhook receiver endpoint
utils.py        — Shared formatting, error handling, and file export utilities
config.py       — Environment variable loading
.env            — Credentials (not committed to version control)

## What's Next

Expand the webhook receiver to handle multiple Plaid webhook types and trigger 
different data pulls based on the event — for example, automatically fetching 
updated transactions when a DEFAULT_UPDATE webhook arrives and generating a 
fresh report. Add filtering options to expose only specific account types or 
transaction categories via command line flags.