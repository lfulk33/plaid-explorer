import json
def handle_plaid_error(e):
    error = json.loads(e.body)
    error_code = error['error_code']
    if (error_code == "INVALID_API_KEYS"):
        print("Error: Authentication failed. Check your Plaid credentials in .env")
    elif (error_code == "INVALID_ACCESS_TOKEN"):
        print("Error: Access token invalid or expired. Re-run the token exchange.")
    else:
        print(f"Unexpected Plaid error: {error_code} - {error.get('error_message', '')}")