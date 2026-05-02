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

#Groups by category, sums amounts, sorts descending. Returns top 3 categories, count over $100, total spend
def analyze_transactions(transactions): 
    sum_by_cat = {}
    trans_over_100 = 0
    total_spend = 0
    for transaction in transactions:
        sum_by_cat[str(transaction['personal_finance_category']['primary'])] = sum_by_cat.get(str(transaction['personal_finance_category']['primary']), 0) + transaction['amount']
        if(transaction['amount'] > 100):
            trans_over_100 += 1
        total_spend += transaction['amount']
    sorted_sum_by_cat = sorted(sum_by_cat.items(), key=lambda x: x[1], reverse=True)
    
    return {"sum_by_cat": sorted_sum_by_cat[:3], "trans_over_100": trans_over_100, "total_spend": total_spend}
