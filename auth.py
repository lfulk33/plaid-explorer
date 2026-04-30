from config import get_config
import plaid
from utils import handle_plaid_error
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest


def get_plaid_client():
    env_map = {
        'sandbox': plaid.Environment.Sandbox,
        'production': plaid.Environment.Production
    }
    config = get_config()
    configuration = plaid.Configuration(
        host=env_map.get(config['env'], plaid.Environment.Sandbox),
        api_key={
            'clientId': config['client_id'],
            'secret': config['secret'],
        }
    )
    try:    
        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        return client
    except plaid.ApiException as e:
        handle_plaid_error(e)
        return None
    except Exception as e:
        # Network errors, timeouts, anything else
        print(f"Network or unexpected error: {e}")
        return None         



def create_link_token(client, client_name="Plaid Explorer", country_codes=[CountryCode('US')], language="en", client_user_id="test-user-123"):
    request = LinkTokenCreateRequest(
        products=[Products('transactions')],
        client_name=client_name,
        country_codes=country_codes,
        language=language,
        user=LinkTokenCreateRequestUser(
            client_user_id=client_user_id
        )
    )
    
    try:
        # Perform the API call
        response = client.link_token_create(request)
        # The link_token to pass to your frontend
        return response['link_token']
    except plaid.ApiException as e:
        handle_plaid_error(e)
        return None
    except Exception as e:
        # Network errors, timeouts, anything else
        print(f"Network or unexpected error: {e}")
        return None         


def create_sandbox_public_token(client):
    pt_request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",
        initial_products=[Products('transactions')]
    )
    try:
        pt_response = client.sandbox_public_token_create(pt_request)
        return pt_response['public_token']
    except plaid.ApiException as e:
        handle_plaid_error(e)
        return None
    except Exception as e:
        # Network errors, timeouts, anything else
        print(f"Network or unexpected error: {e}")
        return None         



def exchange_public_token(client, public_token):
    exchange_request = ItemPublicTokenExchangeRequest(public_token)
    try:
        # Perform the API call
        exchange_response = client.item_public_token_exchange(exchange_request)
        # The access_token returned
        return exchange_response['access_token']
    except plaid.ApiException as e:
        handle_plaid_error(e)
        return None
    except Exception as e:
        # Network errors, timeouts, anything else
        print(f"Network or unexpected error: {e}")
        return None         

