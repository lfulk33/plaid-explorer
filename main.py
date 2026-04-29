from auth import get_plaid_client, create_link_token, create_sandbox_public_token, exchange_public_token

client = get_plaid_client()
token = create_link_token(client)
public_token = create_sandbox_public_token(client)
access_token = exchange_public_token(client, public_token)
print(token)
print(public_token)
print(access_token)