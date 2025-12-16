# back/app/TechAgent/sku_repository.py

from typing import List, Dict


# --------------------------------------------------
# OEM SKU DATABASE (Synthetic but Realistic)
# --------------------------------------------------

_SKU_DATABASE: List[Dict] = [
    {
        "sku_id": "APC_HT_11KV_AL_XLPE_3C_A",
        "product_type": "power cable",
        "voltage_kv": 11,
        "conductor": "aluminium",
        "cores": 3,
        "insulation": "xlpe",
        "armouring": "armoured",
        "standard": "is 7098"
    },
    {
        "sku_id": "APC_HT_11KV_CU_XLPE_3C_B",
        "product_type": "power cable",
        "voltage_kv": 11,
        "conductor": "copper",
        "cores": 3,
        "insulation": "xlpe",
        "armouring": "armoured",
        "standard": "is 7098"
    },
    {
        "sku_id": "APC_HT_11KV_AL_PVC_3C_C",
        "product_type": "power cable",
        "voltage_kv": 11,
        "conductor": "aluminium",
        "cores": 3,
        "insulation": "pvc",
        "armouring": "armoured",
        "standard": "is 7098"
    },
    {
        "sku_id": "APC_HT_33KV_AL_XLPE_3C_D",
        "product_type": "power cable",
        "voltage_kv": 33,
        "conductor": "aluminium",
        "cores": 3,
        "insulation": "xlpe",
        "armouring": "armoured",
        "standard": "iec 60502"
    },
    {
        "sku_id": "APC_LT_1KV_AL_XLPE_4C_E",
        "product_type": "power cable",
        "voltage_kv": 1,
        "conductor": "aluminium",
        "cores": 4,
        "insulation": "xlpe",
        "armouring": "unarmoured",
        "standard": "is 7098"
    }
]


# --------------------------------------------------
# PUBLIC ACCESS FUNCTION
# --------------------------------------------------

def get_all_skus() -> List[Dict]:
    """
    Returns all OEM SKUs available for matching.
    """
    return _SKU_DATABASE.copy()
