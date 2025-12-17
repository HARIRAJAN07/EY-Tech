import imaplib
import email
import os
from email.header import decode_header
from dotenv import load_dotenv

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

EMAIL = os.getenv("GMAIL_ID")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# --------------------------------------------------
# Config
# --------------------------------------------------
SAVE_DIR = "data/email_rfp"
RFP_KEYWORDS = ["rfp", "request for proposal", "tender", "bid", "proposal"]

os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# Helper: decode email headers safely
# --------------------------------------------------
def decode_mime(s):
    if not s:
        return ""
    decoded = decode_header(s)
    result = ""
    for part, enc in decoded:
        if isinstance(part, bytes):
            result += part.decode(enc or "utf-8", errors="ignore")
        else:
            result += part
    return result

# --------------------------------------------------
# MAIN FUNCTION (called from API later)
# --------------------------------------------------
def fetch_rfp_from_email(limit=2):
    print("📩 Connecting to Gmail...")

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, APP_PASSWORD)
    imap.select("inbox")

    status, data = imap.search(None, "ALL")
    msg_ids = data[0].split()[-limit:]

    downloaded_files = []

    for mid in msg_ids:
        _, msg_data = imap.fetch(mid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject = decode_mime(msg.get("Subject", "")).lower()

        # ✅ Check RFP keywords
        if any(k in subject for k in RFP_KEYWORDS):
            print(f"✅ RFP Mail Found → {subject}")

            if msg.is_multipart():
                for part in msg.walk():
                    filename = part.get_filename()
                    if filename and filename.lower().endswith(".pdf"):
                        filename = decode_mime(filename)
                        path = os.path.join(SAVE_DIR, filename)

                        with open(path, "wb") as f:
                            f.write(part.get_payload(decode=True))

                        downloaded_files.append(path)
                        print(f"📄 Saved: {path}")

    imap.logout()

    return downloaded_files
def ingest_email_rfps(limit=20):
    """
    API-facing function to ingest RFP PDFs from email
    """
    return fetch_rfp_from_email(limit)