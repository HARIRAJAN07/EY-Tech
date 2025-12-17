from fastapi.responses import FileResponse, Response
from fastapi import APIRouter
from app.BidGenerator.bid_assembler import build_final_bid_json
from app.BidGenerator.bid_pdf_generator import generate_bid_pdf

router = APIRouter(prefix="/bid", tags=["Bid Generator"])


@router.post("/download")
def download_final_bid(payload: dict):

    bid_json = build_final_bid_json(
        rfp_file=payload["rfp_file"],
        technical_requirements=payload["technical_requirements"],

        # ✅ FIX HERE
        final_recommendation=payload["final_tech_decision"],

        pricing_summary=payload["pricing_summary"]
    )

    pdf_path = generate_bid_pdf(bid_json)

    response = FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=pdf_path.split("/")[-1]
    )

    # CORS headers for file
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response
