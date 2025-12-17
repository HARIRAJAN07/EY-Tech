# back/app/BidGenerator/bid_pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os
from datetime import datetime


def generate_bid_pdf(bid_json: dict) -> str:
    """
    Generates Final Bid PDF from structured JSON.
    Returns absolute file path of generated PDF.
    """

    # -------------------------------
    # File setup
    # -------------------------------
    output_dir = "generated_bids"
    os.makedirs(output_dir, exist_ok=True)

    bid_id = bid_json["bid_meta"]["bid_id"]
    file_name = f"{bid_id}_Final_Bid.pdf"
    file_path = os.path.join(output_dir, file_name)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # -------------------------------
    # COVER PAGE
    # -------------------------------
    elements.append(Paragraph("<b>FINAL BID DOCUMENT</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    meta = bid_json["bid_meta"]
    elements.append(Paragraph(f"<b>Project:</b> {meta['rfp_file']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Client:</b> {meta['client_name']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Bid ID:</b> {meta['bid_id']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Date:</b> {meta['submission_date']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Validity:</b> {meta['bid_validity_days']} days", styles["Normal"]))

    elements.append(Spacer(1, 40))

    # -------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------
    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    exec_sum = bid_json["executive_summary"]
    elements.append(Paragraph(exec_sum["project_overview"], styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        f"<b>Recommended SKU:</b> {exec_sum['recommended_sku']}",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        f"<b>Total Bid Value:</b> ₹ {exec_sum['total_bid_value']:,}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 15))

    for point in exec_sum["key_highlights"]:
        elements.append(Paragraph(f"- {point}", styles["Normal"]))

    elements.append(Spacer(1, 25))

    # -------------------------------
    # SCOPE OF SUPPLY
    # -------------------------------
    elements.append(Paragraph("<b>Scope of Supply</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    scope_data = [["Item", "Description", "Quantity", "UOM"]]
    for item in bid_json["scope_of_supply"]:
        scope_data.append([
            item["item"],
            item["description"],
            str(item["quantity"]),
            item["uom"]
        ])

    scope_table = Table(scope_data, hAlign="LEFT")
    scope_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
    ]))
    elements.append(scope_table)

    elements.append(Spacer(1, 25))

    # -------------------------------
    # TECHNICAL SUMMARY
    # -------------------------------
    elements.append(Paragraph("<b>Technical Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    tech = bid_json["technical_summary"]
    elements.append(Paragraph(
        f"Selected SKU: <b>{tech['selected_sku']}</b>",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        f"Match Score: {tech['match_score_percent']}%",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        f"Reason: {tech['selection_reason']}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 15))

    comp_data = [["Specification", "RFP", "Offered"]]
    for row in tech["rfp_vs_offered"]:
        comp_data.append([row["spec"], row["rfp"], row["offered"]])

    comp_table = Table(comp_data, hAlign="LEFT")
    comp_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
    ]))
    elements.append(comp_table)

    elements.append(Spacer(1, 25))

    # -------------------------------
    # PRICING SUMMARY
    # -------------------------------
    elements.append(Paragraph("<b>Commercial Pricing Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    price = bid_json["pricing_summary"]
    pricing_data = [
        ["Component", "Amount (₹)"],
        ["Material Cost", f"{price['material_cost']:,}"],
        ["Testing Cost", f"{price['testing_cost']:,}"],
        ["Packing Cost", f"{price['packing_cost']:,}"],
        ["Transport Cost", f"{price['transport_cost']:,}"],
        ["TOTAL", f"{price['total_cost']:,}"]
    ]

    pricing_table = Table(pricing_data, hAlign="LEFT")
    pricing_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("BACKGROUND", (0, -1), (-1, -1), colors.beige)
    ]))
    elements.append(pricing_table)

    elements.append(Spacer(1, 30))

    # -------------------------------
    # FINAL DECLARATION
    # -------------------------------
    decl = bid_json["final_declaration"]
    elements.append(Paragraph("<b>Final Declaration</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(decl["recommendation"], styles["Normal"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        f"Authorized Signatory: <b>{decl['authorized_signatory']}</b>",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        decl["designation"],
        styles["Normal"]
    ))

    # -------------------------------
    # BUILD PDF
    # -------------------------------
    doc.build(elements)

    return file_path
