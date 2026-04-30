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

#returns "$1,203.42", handles None
def format_currency(amount): 
    return f"${amount:,.2f}"
    
#consistent readable format
def format_date(date_string):
    return date_string.strftime('%b %d, %Y')

##separator line between output sections
def get_divider():
    return " | "