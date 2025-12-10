from fastapi import APIRouter

from app.Ingestion.email_read import ingest_email_rfps
from app.Ingestion.website_read import ingest_website_rfps
from app.Processing.pdf_extract import parse_all_rfps
from app.Scoring.rfp_scores import score_and_rank_rfps


router = APIRouter(prefix="/rfp", tags=["RFP"])


@router.post("/check")
def check_rfps():
    """
    ✅ Sales Agent Trigger (END TO END)
    1. Fetch RFP PDFs (Email + Website)
    2. Parse PDFs
    3. Score & Rank RFPs
    """

    # 1️⃣ INGESTION
    email_files = ingest_email_rfps(limit=20)
    website_files = ingest_website_rfps()

    # 2️⃣ PARSING
    rfp_records = parse_all_rfps()

    # 3️⃣ SCORING & RANKING
    ranked_rfps = score_and_rank_rfps(rfp_records)

    return {
        "status": "success",
        "message": "RFP ingestion + scoring completed",

        "email_rfps_found": len(email_files),
        "website_rfps_found": len(website_files),
        "total_rfps": len(ranked_rfps),

        # ⭐ FRONTEND READY
        "top_3": ranked_rfps[:3],
        "others": ranked_rfps[3:]
    }
