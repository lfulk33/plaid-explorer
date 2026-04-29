import plaid
from plaid.model.accounts_get_request import AccountsGetRequest

def get_accounts(client, access_token):
    try:
        request = AccountsGetRequest(access_token=access_token)
        response = client.accounts_get(request)
        return response['accounts']
    except plaid.ApiException as e:
        print(f"Error getting accounts: {e}")
        return None

