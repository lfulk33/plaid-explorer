from auth import get_plaid_client, create_link_token, create_sandbox_public_token, exchange_public_token
from accounts import get_accounts, get_account_health
from transactions import get_transactions
from utils import format_currency, get_divider, format_date
import time

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
accounts = get_accounts(client, access_token)

if accounts:
    for account in accounts:
        if(account['balances']['current']):
            print(f"{account['name']}{get_divider()}{account['type']}{get_divider()}{format_currency(account['balances']['current'])}")
        else:
            print(f"{account['name']}{get_divider()}{account['type']}{get_divider()}Empty")
else:
    print("There are no accounts listed")

time.sleep(5)

transactions = get_transactions(client, access_token, limit = 5)
if transactions:
    for transaction in transactions:
        merchant = transaction['merchant_name'] or transaction['name']
        print(f"{format_date(transaction['date'])}{get_divider()}{merchant}{get_divider()}{format_currency(transaction['amount'])}{get_divider()}{transaction['personal_finance_category']['primary']}")
else:
    print("There are no transactions listed")

account_health = get_account_health(accounts)
print("===== ACCOUNT HEALTH SUMMARY =====")
print(f"Total Balance: {format_currency(account_health['total_balance'])}")
print("Accounts: " + ', '.join([f"{count} {type_name}" for type_name, count in account_health['count_by_type'].items()]))
if (len(account_health['flagged']) > 0):
    print("Flagged: " + ', '.join([f"{name} ({format_currency(balance)}) - negative balance" for name, balance in account_health['flagged'].items()]))
else:
    print("Flagged: None")