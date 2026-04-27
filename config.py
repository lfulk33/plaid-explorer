from dotenv import load_dotenv
import os

def get_config():
    load_dotenv()
    return {
        'client_id': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET'),
        'env': os.getenv('PLAID_ENV')
    }