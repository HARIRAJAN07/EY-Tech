# back/app/TechAgent/final_decision.py

from typing import Dict, List


def select_final_sku(
    rfp_specs: Dict,
    matched_skus: List[Dict]
) -> Dict:
    """
    Selects the best SKU based on:
    1. Highest spec match score
    2. Closest voltage match (tie-breaker)
    """

    if not matched_skus:
        return {
            "status": "no_match",
            "reason": "No suitable OEM SKUs found"
        }

    best_score = matched_skus[0]["score_percent"]

    top_candidates = [
        sku for sku in matched_skus
        if sku["score_percent"] == best_score
    ]

    # If only one best candidate → return
    if len(top_candidates) == 1:
        chosen = top_candidates[0]
    else:
        # Tie-breaker: closest voltage
        rfp_voltage = rfp_specs.get("voltage_kv")

        def voltage_distance(sku):
            sku_voltage = sku["sku_data"].get("voltage_kv")
            if rfp_voltage is None or sku_voltage is None:
                return float("inf")
            return abs(sku_voltage - rfp_voltage)

        chosen = sorted(top_candidates, key=voltage_distance)[0]

    # ✅ NORMALIZED, PRICING-READY OUTPUT
    return {
        "selected_sku": chosen["sku_id"],
        "sku_specs": {
            "product_type": chosen["sku_data"]["product_type"],
            "voltage_kv": chosen["sku_data"]["voltage_kv"],
            "conductor": chosen["sku_data"]["conductor"],
            "cores": chosen["sku_data"]["cores"],
            "insulation": chosen["sku_data"]["insulation"],
            "armouring": chosen["sku_data"]["armouring"],
            "standard": chosen["sku_data"]["standard"],
        },
        "decision_meta": {
            "score_percent": chosen["score_percent"],
            "reason": "Highest spec match with closest voltage alignment"
        }
    }
