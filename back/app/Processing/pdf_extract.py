# back/app/Processing/pdf_parser.py

import os
import pdfplumber
import re

# --------------------------------------------------
# CONFIG (Backend-safe paths)
# --------------------------------------------------
EMAIL_DIR = "data/email_rfp"
WEB_DIR = "data/website_rfp"

# --------------------------------------------------
# 1️⃣ Collect all PDFs
# --------------------------------------------------
def collect_all_pdfs():
    pdfs = []
    for folder in [EMAIL_DIR, WEB_DIR]:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.lower().endswith(".pdf"):
                    pdfs.append(os.path.join(folder, f))
    return pdfs

# --------------------------------------------------
# 2️⃣ Extract clean lines from PDF
# --------------------------------------------------
def extract_lines(pdf_path):
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.split("\n"))
    return [l.strip() for l in lines if l.strip()]

# --------------------------------------------------
# Helper: find first matching line
# --------------------------------------------------
def find_first(predicate, lines):
    for l in lines:
        if predicate(l):
            return l
    return ""

# --------------------------------------------------
# 3️⃣ MAIN PARSER FUNCTION (🔥 CORE FUNCTION)
# --------------------------------------------------
def parse_all_rfps():
    records = []
    pdf_files = collect_all_pdfs()

    for pdf in pdf_files:
        lines = extract_lines(pdf)
        text_lower = " ".join(lines).lower()

        # BASIC INFO
        organization = find_first(
            lambda l: any(k in l.lower() for k in [
                "authority", "corporation", "ltd", "limited", "agency"
            ]),
            lines
        )

        rfp_no = find_first(lambda l: "rfp/" in l.lower(), lines)
        issue_date = find_first(lambda l: "issue" in l.lower() and "date" in l.lower(), lines)
        deadline = find_first(
            lambda l: "deadline" in l.lower() or "last date" in l.lower(),
            lines
        )

        email = find_first(lambda l: "@" in l, lines)

        # OVERVIEW
        overview = find_first(
            lambda l: any(w in l.lower() for w in [
                "procurement", "supply", "design", "manufacture"
            ]),
            lines
        )

        # SCOPE OF SUPPLY
        scope_lines = []
        capture = False
        for l in lines:
            if "scope of supply" in l.lower() or "scope of work" in l.lower():
                capture = True
                continue
            if capture and re.match(r"\d+\.", l):
                break
            if capture:
                scope_lines.append(l)

        scope_text = " ".join(scope_lines)

        # EQUIPMENT
        equipment = list(set(re.findall(
            r"(transformer[s]?|cable[s]?|switchgear|panel[s]?|substation[s]?)",
            scope_text.lower()
        )))

        # QUANTITY
        quantities = re.findall(
            r"(\d+)\s*(units?|sets?|lots?|nos|km)",
            scope_text.lower()
        )

        # RATINGS
        ratings = re.findall(
            r"(\d+\/\d+\s*kv|\d+\s*kv|\d+\s*mw|\d+\s*mva)",
            scope_text.lower()
        )

        records.append({
            "file_name": os.path.basename(pdf),
            "organization": organization,
            "rfp_reference": rfp_no,
            "issue_date": issue_date,
            "submission_deadline": deadline,
            "overview": overview,
            "equipment": equipment,
            "quantity": quantities,
            "ratings": ratings,
            "email": email
        })

    return records
