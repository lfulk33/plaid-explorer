from auth import get_plaid_client, create_link_token, create_sandbox_public_token, exchange_public_token
from accounts import get_accounts, get_account_health
from transactions import get_transactions, analyze_transactions
from utils import format_currency, get_divider, format_date, save_report, print_account_list, print_transaction_list, print_account_summary, print_transaction_summary
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--days', type=int, default=30)
parser.add_argument('--limit', type=int, default=10)
parser.add_argument('--save', action='store_true')
args = parser.parse_args()

# --- Authentication Flow ---
client = get_plaid_client()
token = create_link_token(client)
if token is None:
    print("Failed to create token. Exiting.")
    exit()
public_token = create_sandbox_public_token(client)
if public_token is None:
    print("Failed to create public token. Exiting.")
    exit()
access_token = exchange_public_token(client, public_token)
if access_token is None:
    print("Failed to exchange public token. Exiting.")
    exit()

# Account Data
accounts = get_accounts(client, access_token)
print_account_list(accounts)

# Transaction Data
time.sleep(5)
transactions = get_transactions(client, access_token, args.days, args.limit)
print_transaction_list(transactions)

# Analysis
account_health = get_account_health(accounts)
print_account_summary(accounts, account_health)

analyzed = analyze_transactions(transactions)
print_transaction_summary(transactions, analyzed)

if (args.save):
    filename = save_report(account_health, analyzed)
    print(f"Report saved to {filename}")
