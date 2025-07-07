
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup koneksi Google Sheets
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDENTIALS_FILE = "gdrive_secret.json"

try:
    CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(CREDS)
    SHEET_NAME = "Planville Leads"
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    sheet = None
    print(f"[WARNING] Tidak bisa konek ke Google Sheets: {e}")

def capture_lead(message: str, lang: str, intent: str):
    if not sheet:
        print("[SKIP] Google Sheets tidak tersedia")
        return
    timestamp = datetime.now().isoformat()
    try:
        sheet.append_row([timestamp, message, lang, intent])
        print(f"[LEAD] Captured: {message} - {lang} - {intent}")
    except Exception as e:
        print(f"[ERROR] Gagal simpan lead: {e}")

def capture_feedback(message: str, lang: str, label: str = "positif"):
    if not sheet:
        print("[SKIP] Sheet tidak tersedia untuk feedback.")
        return
    timestamp = datetime.now().isoformat()
    try:
        sheet.append_row([timestamp, message, lang, f"FEEDBACK-{label}"])
        print(f"[FEEDBACK] Captured: {message} - {lang} - {label}")
    except Exception as e:
        print(f"[ERROR] Gagal simpan feedback: {e}")
