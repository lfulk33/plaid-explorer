from config import get_config
import plaid
from plaid.api import plaid_api


def get_plaid_client():
    config = get_config()
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={
            'clientId': config['client_id'],
            'secret': config['secret'],
        }
    )

    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    return client