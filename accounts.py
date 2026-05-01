import plaid
from utils import handle_plaid_error
from plaid.model.accounts_get_request import AccountsGetRequest

def get_accounts(client, access_token):
    try:
        request = AccountsGetRequest(access_token=access_token)
        response = client.accounts_get(request)
        return response['accounts']
    except plaid.ApiException as e:
        handle_plaid_error(e)
        return None
    except Exception as e:
        # Network errors, timeouts, anything else
        print(f"Network or unexpected error: {e}")
        return None         

#get_account_health(accounts): Returns total balance, count by type, and any accounts with zero or negative balance flagged.
def get_account_health(accounts):
    total_balance = 0
    count_by_type = {}
    flagged = {}
    for account in accounts:
        total_balance += float(account['balances']['current'])
        count_by_type[str(account['type'])] = count_by_type.get(str(account['type']), 0) +1
        if (account['balances']['current'] < 0):
            #sandbox data has no negative balances so the flagged list will be empty in testing
            flagged[str(account['name'])] = float(account['balances']['current'])
    return {"total_balance": total_balance, "count_by_type": count_by_type, "flagged": flagged}

