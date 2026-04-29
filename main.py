from auth import get_plaid_client, create_link_token, create_sandbox_public_token, exchange_public_token
from accounts import get_accounts

client = get_plaid_client()
token = create_link_token(client)
public_token = create_sandbox_public_token(client)
access_token = exchange_public_token(client, public_token)
accounts = get_accounts(client, access_token)
for account in accounts:
    if(account['balances']['current']):
        print(f"{account['name']} | {account['type']} | ${account['balances']['current']:,.2f}")
    else:
        print(f"{account['name']} | {account['type']} | Empty}")