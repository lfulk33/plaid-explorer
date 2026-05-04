import json
import os
from datetime import datetime, date

# Parses Plaid API exceptions and prints a human-readable error message
def handle_plaid_error(e):
    error = json.loads(e.body)
    error_code = error['error_code']
    if (error_code == "INVALID_API_KEYS"):
        print("Error: Authentication failed. Check your Plaid credentials in .env")
    elif (error_code == "INVALID_ACCESS_TOKEN"):
        print("Error: Access token invalid or expired. Re-run the token exchange.")
    else:
        print(f"Unexpected Plaid error: {error_code} - {error.get('error_message', '')}")

#returns "$1,203.42", handles None
def format_currency(amount): 
    return f"${amount:,.2f}"
    
#consistent readable format
def format_date(date_string):
    return date_string.strftime('%b %d, %Y')

#separator line between output sections
def get_divider():
    return " | "

#helper function to write line w/ new line
def writeln(f, text):
    f.write(text + '\n')

def print_account_list(accounts):
    if accounts:
        for account in accounts:
            if(account['balances']['current']):
                print(f"{account['name']}{get_divider()}{account['type']}{get_divider()}{format_currency(account['balances']['current'])}")
            else:
                print(f"{account['name']}{get_divider()}{account['type']}{get_divider()}Empty")
    else:
        print("There are no accounts listed")

def print_transaction_list(transactions):
    if transactions:
        for transaction in transactions:
            merchant = transaction['merchant_name'] or transaction['name']
            print(f"{format_date(transaction['date'])}{get_divider()}{merchant}{get_divider()}{format_currency(transaction['amount'])}{get_divider()}{transaction['personal_finance_category']['primary']}")
    else:
        print("There are no transactions listed")

# Prints formatted account list and health summary to the terminal
def print_account_summary(accounts, account_health):
    print("===== ACCOUNT HEALTH SUMMARY =====")
    print(f"Total Balance: {format_currency(account_health['total_balance'])}")
    print("Accounts: " + ', '.join([f"{count} {type_name}" for type_name, count in account_health['count_by_type'].items()]))
    if (len(account_health['flagged']) > 0):
        print("Flagged: " + ', '.join([f"{name} ({format_currency(balance)}) - negative balance" for name, balance in account_health['flagged'].items()]))
    else:
        print("Flagged: None")

# Prints formatted transaction analysis to the terminal  
def print_transaction_summary(transactions, analyzed):
    print("===== TRANSACTION ANALYSIS =====")
    print("Top Spending Categories:")
    x = 1
    for category, sum in analyzed['sum_by_cat']:
        print(f"{x}. {category.replace('_', ' ').title():<20} {format_currency(sum):>10}")
        x = x + 1
    print(f"Large transactions (over $100): {analyzed['trans_over_100']}")
    print(f"Total spend (30 days): {format_currency(analyzed['total_spend'])}")
    
#Saves to reports/report_YYYYMMDD_HHMMSS.txt. Creates reports/ if needed. Returns the filename.
def save_report(account_summary, transaction_analysis): 
    path = "reports"
    os.makedirs(path, exist_ok=True)
    filename = path + "/report_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".txt"
    with open(filename, "w") as f:
        writeln(f, "===== ACCOUNT HEALTH SUMMARY =====")
        writeln(f, f"Total Balance: {format_currency(account_summary['total_balance'])}")
        writeln(f,"Accounts: " + ', '.join([f"{count} {type_name}" for type_name, count in account_summary['count_by_type'].items()]))
        if (len(account_summary['flagged']) > 0):
            writeln(f,"Flagged: " + ', '.join([f"{name} ({format_currency(balance)}) - negative balance" for name, balance in account_summary['flagged'].items()]))
        else:
            writeln(f,"Flagged: None")

        writeln(f,"===== TRANSACTION ANALYSIS =====")
        writeln(f,"Top Spending Categories:")
        x = 1
        for category, sum in transaction_analysis['sum_by_cat']:
            writeln(f,f"{x}. {category.replace('_', ' ').title():<20} {format_currency(sum):>10}")
            x = x + 1
        writeln(f,f"Large transactions (over $100): {transaction_analysis['trans_over_100']}")
        writeln(f,f"Total spend (30 days): {format_currency(transaction_analysis['total_spend'])}")

    return filename