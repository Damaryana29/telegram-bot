import json
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Memuat variabel dari file .env
load_dotenv()

# Menentukan direktori file ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path ke file kredensial dan konfigurasi
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# Debug: Cek apakah path benar
print("CREDENTIALS_PATH:", CREDENTIALS_PATH)

def load_config():
    """Memuat konfigurasi dari config.json"""
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_config(data):
    """Menyimpan konfigurasi ke config.json"""
    with open(CONFIG_PATH, "w") as file:
        json.dump(data, file, indent=4)

# Token dan kredensial bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Menggunakan path yang lebih aman
if os.path.exists(CREDENTIALS_PATH):
    print("✅ File credentials.json ditemukan!")  # Debugging tambahan
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
else:
    creds = None
    print("\u26A0\ufe0f File kredensial tidak ditemukan! Pastikan 'credentials.json' ada di folder 'config/'.")

# Memuat konfigurasi spreadsheet
config = load_config()
SPREADSHEET_ID = config.get("spreadsheet_id", "")
SHEET_NAME = "Result"
