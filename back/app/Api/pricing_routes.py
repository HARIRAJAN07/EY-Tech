from fastapi import APIRouter
from app.PricingAgent.pricing_logic import calculate_pricing

router = APIRouter(prefix="/pricing", tags=["Pricing Agent"])


@router.post("/calculate")
def pricing_agent(payload: dict):
    try:
        pricing = calculate_pricing(
            payload["final_recommendation"],
            payload.get("quantity", 10)
        )
        return {
            "status": "success",
            "pricing_summary": pricing
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
