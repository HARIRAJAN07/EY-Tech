# back/app/TechAgent/pdf_parser.py

import pdfplumber
import re
from typing import Dict, List


# --------------------------------------------------
# Internal helpers
# --------------------------------------------------

def _normalize(text: str) -> str:
    return (
        text.lower()
        .replace("k.v", "kv")
        .replace("kv", " kv")
        .replace("-", " ")
    )


def _extract_lines(pdf_path: str) -> List[str]:
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(
                    [l.strip() for l in text.split("\n") if l.strip()]
                )
    return lines


# --------------------------------------------------
# Individual spec extractors
# --------------------------------------------------

def _extract_voltage(text: str):
    match = re.search(r"(\d{1,3})\s*kv", text)
    return int(match.group(1)) if match else None


def _extract_conductor(text: str):
    if "aluminium" in text or "aluminum" in text:
        return "aluminium"
    if "copper" in text:
        return "copper"
    return None


def _extract_cores(text: str):
    match = re.search(r"(\d(\.\d)?)\s*core", text)
    return float(match.group(1)) if match else None


def _extract_insulation(text: str):
    if "xlpe" in text:
        return "xlpe"
    if "pvc" in text:
        return "pvc"
    return None


def _extract_armouring(text: str):
    if "unarmoured" in text or "unarmored" in text:
        return "unarmoured"
    if "armoured" in text or "armored" in text:
        return "armoured"
    return None


def _extract_standard(text: str):
    if "is 7098" in text:
        return "is 7098"
    if "iec 60502" in text:
        return "iec 60502"
    return None


def _extract_quantity(text: str):
    match = re.search(r"(\d+(\.\d+)?)\s*(km|kilometre|kilometer)", text)
    return f"{match.group(1)} km" if match else None


# --------------------------------------------------
# PUBLIC FUNCTION (Tech Agent Contract)
# --------------------------------------------------

def parse_technical_specs(pdf_path: str) -> Dict:
    """
    Parse technical specifications from an RFP PDF.
    Returns a normalized technical requirement dictionary.
    """

    lines = _extract_lines(pdf_path)
    normalized_text = " ".join(_normalize(l) for l in lines)

    return {
        "product_type": "power cable",
        "voltage_kv": _extract_voltage(normalized_text),
        "conductor": _extract_conductor(normalized_text),
        "cores": _extract_cores(normalized_text),
        "insulation": _extract_insulation(normalized_text),
        "armouring": _extract_armouring(normalized_text),
        "standard": _extract_standard(normalized_text),
        "quantity": _extract_quantity(normalized_text),
    }
