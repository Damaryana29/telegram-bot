import gspread
from config.config import creds, SPREADSHEET_ID, SHEET_NAME, load_config, save_config

def get_client():
    return gspread.authorize(creds)

def get_sheet():
    client = get_client()
    if SPREADSHEET_ID:
        return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    return None

def update_spreadsheet_id(new_id):
    config = load_config()
    config["spreadsheet_id"] = new_id
    save_config(config)
    global SPREADSHEET_ID
    SPREADSHEET_ID = new_id
    return get_sheet()

