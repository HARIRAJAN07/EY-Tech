# back/app/TechAgent/matcher.py

from typing import Dict, List, Tuple


# --------------------------------------------------
# Specs to compare (equal weight)
# --------------------------------------------------

_COMPARABLE_SPECS = [
    "voltage_kv",
    "conductor",
    "cores",
    "insulation",
    "armouring",
    "standard"
]


# --------------------------------------------------
# Internal helper
# --------------------------------------------------

def _compute_match_score(
    rfp_specs: Dict,
    sku: Dict
) -> Tuple[float, Dict[str, str]]:
    matched = 0
    total = 0
    breakdown = {}

    for spec in _COMPARABLE_SPECS:
        rfp_val = rfp_specs.get(spec)

        # Skip specs not mentioned in RFP
        if rfp_val is None:
            continue

        total += 1
        sku_val = sku.get(spec)

        if sku_val == rfp_val:
            matched += 1
            breakdown[spec] = "MATCH"
        else:
            breakdown[spec] = f"NO MATCH (RFP={rfp_val}, SKU={sku_val})"

    score = round((matched / total) * 100, 2) if total > 0 else 0.0
    return score, breakdown


# --------------------------------------------------
# PUBLIC FUNCTION
# --------------------------------------------------

def match_skus(
    rfp_specs: Dict,
    skus: List[Dict]
) -> List[Dict]:
    """
    Compute spec match score for each SKU.
    Returns sorted list (highest score first).
    """

    results = []

    for sku in skus:
        score, breakdown = _compute_match_score(rfp_specs, sku)

        results.append({
            "sku_id": sku["sku_id"],
            "score_percent": score,
            "breakdown": breakdown,
            "sku_data": sku
        })

    return sorted(results, key=lambda x: x["score_percent"], reverse=True)
