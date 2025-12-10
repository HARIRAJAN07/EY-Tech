import requests
import os

# --------------------------------------------------
# Config
# --------------------------------------------------
BASE_URL = "https://dummy-website-rfp.netlify.app/rfps/"
SAVE_DIR = "data/website_rfp"

os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# PUBLIC FUNCTION
# --------------------------------------------------
def ingest_website_rfps():
    """
    Fetch RFP PDFs from hosted website
    """
    downloaded_files = []

    # ✅ For prototype, we know filenames
    for i in range(1, 9):
        filename = f"rfp_{i:02}.pdf"
        url = f"{BASE_URL}{filename}"
        path = os.path.join(SAVE_DIR, filename)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(path, "wb") as f:
                f.write(response.content)

            downloaded_files.append(path)
            print(f"🌐 Website RFP saved: {path}")

        except Exception as e:
            print(f"❌ Failed to fetch {filename}: {e}")

    return downloaded_files
