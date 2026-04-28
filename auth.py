from config import get_config
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode


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
        print(f"Error creating link token: {e}")
        return None
