from datetime import datetime
import re

TODAY = datetime(2025, 2, 10)

# -------------------------------
# Helper: parse date
# -------------------------------
def parse_date(text):
    try:
        return datetime.strptime(
            re.sub(r"(Issue Date|Submission Deadline)", "", text).strip(),
            "%d %B %Y"
        )
    except:
        return None


# -------------------------------
# Project Value (40)
# -------------------------------
def project_value_score(r):
    score = 0
    reasons = []

    if "transformer" in r["equipment"]:
        score += 15
        reasons.append("High-value capital equipment (transformer)")
    elif any(e in r["equipment"] for e in ["switchgear", "panel", "panels"]):
        score += 12
        reasons.append("Medium-high value electrical equipment")
    elif "cable" in r["equipment"]:
        score += 10
        reasons.append("Large-scale cable supply")
    else:
        score += 5
        reasons.append("Generic electrical scope")

    qty_vals = [int(q[0]) for q in r["quantity"]] if r["quantity"] else []
    max_qty = max(qty_vals) if qty_vals else 0

    if max_qty >= 100:
        score += 15
        reasons.append("Very large quantity")
    elif max_qty >= 50:
        score += 12
        reasons.append("High quantity")
    elif max_qty >= 10:
        score += 8
        reasons.append("Moderate quantity")
    elif max_qty > 0:
        score += 4
        reasons.append("Low quantity")

    rating_text = " ".join(r["ratings"]).lower()
    if "33" in rating_text or "mva" in rating_text:
        score += 10
        reasons.append("High technical rating")
    elif "11kv" in rating_text:
        score += 7
        reasons.append("Medium voltage system")
    elif "1kv" in rating_text:
        score += 4
        reasons.append("Low voltage system")

    return min(score, 40), reasons


# -------------------------------
# Deadline Urgency (35)
# -------------------------------
def deadline_score(r):
    d = parse_date(r["submission_deadline"])
    if not d:
        return 0, ["Deadline missing"]

    days_left = (d - TODAY).days

    if days_left < 0:
        return 0, [f"Expired ({abs(days_left)} days ago)"]
    if days_left <= 15:
        return 35, [f"Critical deadline ({days_left} days left)"]
    elif days_left <= 30:
        return 32, [f"Very urgent ({days_left} days left)"]
    elif days_left <= 45:
        return 28, [f"High urgency"]
    elif days_left <= 60:
        return 24, [f"Moderate urgency"]
    elif days_left <= 90:
        return 18, [f"Comfortable timeline"]
    else:
        return 10, [f"Long-term opportunity"]


# -------------------------------
# Business Relevance (25)
# -------------------------------
def business_relevance_score(r):
    score = 0
    reasons = []
    overview = (r.get("overview") or "").lower()

    if any(k in overview for k in ["utility", "substation", "infrastructure", "power"]):
        score += 15
        reasons.append("Infrastructure / utility project")
    elif any(k in overview for k in ["industrial", "manufacturing"]):
        score += 12
        reasons.append("Industrial project")
    else:
        score += 6
        reasons.append("Generic electrical relevance")

    if any(e in r["equipment"] for e in ["transformer", "cable", "substation"]):
        score += 10
        reasons.append("Strong product alignment")
    else:
        score += 5
        reasons.append("Partial alignment")

    return min(score, 25), reasons


# -------------------------------
# MAIN EXPORT FUNCTION
# -------------------------------
def score_and_rank_rfps(rfp_records):

    for r in rfp_records:
        r["value_score"], v_reason = project_value_score(r)
        r["urgency_score"], u_reason = deadline_score(r)
        r["relevance_score"], b_reason = business_relevance_score(r)

        r["total_score"] = (
            r["value_score"]
            + r["urgency_score"]
            + r["relevance_score"]
        )

        r["status"] = (
            "Expired" if r["urgency_score"] == 0 else
            "High Priority" if r["urgency_score"] >= 28 else
            "Medium Priority" if r["urgency_score"] >= 18 else
            "Low Priority"
        )

        r["explanation"] = {
            "Project Value": v_reason,
            "Deadline Urgency": u_reason,
            "Business Relevance": b_reason
        }

    return sorted(rfp_records, key=lambda x: x["total_score"], reverse=True)
