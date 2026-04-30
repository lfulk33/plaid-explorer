from datetime import datetime, timedelta
import plaid
from utils import handle_plaid_error
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions


#Calculate start_date with datetime. 
#Extract name, amount, date, category. 
# Return list sliced to limit.
def get_transactions(client, access_token, days_back=30, limit=10): 
    #sync is the production recommendation but we'll use get for learning
    start_date = (datetime.now() - timedelta(days=days_back)).date()
    end_date = datetime.now().date()
    days_back = days_back
    limit = limit
    try:
        request = TransactionsGetRequest(
                    access_token = access_token,
                    start_date = start_date,
                    end_date = end_date,
                    options = TransactionsGetRequestOptions(
                        offset = 0,
                        count = limit
                    )
        )
        response = client.transactions_get(request)
        return response['transactions']
    except plaid.ApiException as e:
        handle_plaid_error(e)
        return None
    except Exception as e:
        # Network errors, timeouts, anything else
        print(f"Network or unexpected error: {e}")
        return None         


