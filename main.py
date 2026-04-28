from auth import get_plaid_client, create_link_token

client = get_plaid_client()
token = create_link_token(client)
print(token)