# back/app/Api/tech_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

# Tech Agent modules
from app.TechAgent.pdf_parser import parse_technical_specs
from app.TechAgent.sku_repository import get_all_skus
from app.TechAgent.matcher import match_skus
from app.TechAgent.comparator import build_top3_comparison
from app.TechAgent.final_decision import select_final_sku


# --------------------------------------------------
# Router setup
# --------------------------------------------------
router = APIRouter(prefix="/tech", tags=["Tech Agent"])


# --------------------------------------------------
# Request schema
# --------------------------------------------------
class TechAnalyzeRequest(BaseModel):
    file_name: str


# --------------------------------------------------
# Helper: resolve PDF path
# --------------------------------------------------
def resolve_pdf_path(file_name: str) -> str:
    email_path = os.path.join("data", "email_rfp", file_name)
    website_path = os.path.join("data", "website_rfp", file_name)

    if os.path.exists(email_path):
        return email_path
    if os.path.exists(website_path):
        return website_path

    raise HTTPException(
        status_code=404,
        detail=f"RFP file '{file_name}' not found"
    )


# --------------------------------------------------
# TECH AGENT – END TO END
# --------------------------------------------------
@router.post("/analyze")
def analyze_rfp(req: TechAnalyzeRequest):
    """
    👑 Tech Agent Orchestrator
    Runs full technical analysis for ONE selected RFP
    """

    # 1️⃣ Resolve PDF
    pdf_path = resolve_pdf_path(req.file_name)

    # 2️⃣ Parse technical requirements from RFP
    rfp_specs = parse_technical_specs(pdf_path)

    # 3️⃣ Load OEM SKU repository
    skus = get_all_skus()

    # 4️⃣ Match SKUs against RFP specs
    matched_skus = match_skus(rfp_specs, skus)

    if not matched_skus:
        return {
            "status": "failed",
            "message": "No matching SKUs found",
            "rfp_specs": rfp_specs
        }

    # 5️⃣ Build Top-3 comparison table
    comparison = build_top3_comparison(rfp_specs, matched_skus)

    # 6️⃣ Select final SKU
    final_selection = select_final_sku(rfp_specs, matched_skus)

    # --------------------------------------------------
    # FINAL RESPONSE (Frontend-Ready)
    # --------------------------------------------------
    return {
        "status": "success",
        "rfp_file": req.file_name,

        "technical_requirements": rfp_specs,

        "top_3_recommendations": comparison["top_3_skus"],
        "comparison_table": comparison["comparison_table"],

        "final_recommendation": final_selection
    }
