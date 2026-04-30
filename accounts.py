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

