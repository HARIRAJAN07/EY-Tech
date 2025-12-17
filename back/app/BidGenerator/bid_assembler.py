from datetime import datetime
import uuid


def build_final_bid_json(
    rfp_file: str,
    technical_requirements: dict,
    final_recommendation: dict,
    pricing_summary: dict
) -> dict:

    bid_id = f"BID-{uuid.uuid4().hex[:8].upper()}"

    return {
        # --------------------
        # META
        # --------------------
        "bid_meta": {
            "bid_id": bid_id,
            "rfp_file": rfp_file,
            "client_name": "Confidential Client",
            "submission_date": datetime.today().strftime("%d-%m-%Y"),
            "bid_validity_days": 90
        },

        # --------------------
        # EXECUTIVE SUMMARY
        # --------------------
        "executive_summary": {
            "project_overview": (
                "This bid is submitted in response to the referenced RFP. "
                "The proposed solution meets all mandatory technical "
                "requirements with optimized commercial value."
            ),
            "recommended_sku": final_recommendation["selected_sku"],
            "total_bid_value": pricing_summary["total_cost"],
            "key_highlights": [
                "Compliant with RFP technical specifications",
                "Optimized lifecycle cost",
                "Fast delivery timeline",
                "OEM-tested and certified product"
            ]
        },

        # --------------------
        # SCOPE OF SUPPLY
        # --------------------
        "scope_of_supply": [
            {
                "item": "Power Cable",
                "description": f"{final_recommendation['selected_sku']} as per RFP specs",
                "quantity": pricing_summary["quantity"],
                "uom": pricing_summary["uom"]
            }
        ],

        # --------------------
        # TECHNICAL SUMMARY
        # --------------------
        "technical_summary": {
            "selected_sku": final_recommendation["selected_sku"],
            "match_score_percent": final_recommendation["decision_meta"]["score_percent"],
            "selection_reason": final_recommendation["decision_meta"]["reason"],
            "rfp_vs_offered": [
                {
                    "spec": k,
                    "rfp": technical_requirements.get(k),
                    "offered": v
                }
                for k, v in final_recommendation["sku_specs"].items()
            ]
        },

        # --------------------
        # PRICING
        # --------------------
        "pricing_summary": pricing_summary,

        # --------------------
        # FINAL DECLARATION
        # --------------------
        "final_declaration": {
            "recommendation": (
                "We confirm that the above offer complies fully with the RFP "
                "requirements and is commercially competitive."
            ),
            "authorized_signatory": "Head – B2B Sales",
            "designation": "Authorized Signatory"
        }
    }
