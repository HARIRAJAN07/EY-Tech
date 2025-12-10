# back/app/Api/rfp_routes.py

from fastapi import APIRouter

from app.Ingestion.email_read import fetch_rfp_from_email
from app.Ingestion.website_read import ingest_website_rfps


router = APIRouter(prefix="/rfp", tags=["RFP"])

# --------------------------------------------------
# 1️⃣ Ingest RFPs (Email + Website)
# --------------------------------------------------
@router.post("/ingest")
def ingest_rfps():
    email_files = fetch_rfp_from_email()
    website_files = ingest_website_rfps()

    return {
        "status": "success",
        "message": "RFP ingestion completed",
        "email_rfps_found": len(email_files),
        "website_rfps_found": len(website_files),
        "email_files": email_files,
        "website_files": website_files,
        "total_rfps": len(email_files) + len(website_files)
    }

# --------------------------------------------------
# 2️⃣ Parse all RFP PDFs
# --------------------------------------------------
@router.get("/parse")
def parse_rfps():
    records = parse_all_rfps()

    return {
        "status": "success",
        "total_rfps": len(records),
        "rfps": records
    }
