# back/app/TechAgent/comparator.py

from typing import Dict, List


# --------------------------------------------------
# Specs to display in comparison
# --------------------------------------------------

_COMPARISON_SPECS = [
    "voltage_kv",
    "conductor",
    "cores",
    "insulation",
    "armouring",
    "standard"
]


# --------------------------------------------------
# PUBLIC FUNCTION
# --------------------------------------------------

def build_top3_comparison(
    rfp_specs: Dict,
    matched_skus: List[Dict]
) -> Dict:
    """
    Builds a comparison table for top 3 SKU matches.
    """

    top_3 = matched_skus[:3]

    comparison_rows = []

    for spec in _COMPARISON_SPECS:
        rfp_value = rfp_specs.get(spec)

        # Skip specs not defined in RFP
        if rfp_value is None:
            continue

        row = {
            "spec": spec,
            "rfp_requirement": rfp_value
        }

        for idx, sku in enumerate(top_3, start=1):
            row[f"sku_{idx}"] = sku["sku_data"].get(spec)

        comparison_rows.append(row)

    return {
        "top_3_skus": [
            {
                "sku_id": sku["sku_id"],
                "score_percent": sku["score_percent"]
            }
            for sku in top_3
        ],
        "comparison_table": comparison_rows
    }
