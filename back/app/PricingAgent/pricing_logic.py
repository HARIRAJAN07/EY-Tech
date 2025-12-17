# ============================================================
# PRICING AGENT — LOGIC
# ============================================================

SKU_PRICE_TABLE = {
    "APC_HT_11KV_CU_XLPE_3C_B": {"unit_price": 450000, "uom": "km"},
    "APC_HT_11KV_AL_XLPE_3C_A": {"unit_price": 320000, "uom": "km"},
    "APC_HT_33KV_AL_XLPE_3C_D": {"unit_price": 780000, "uom": "km"},
}

TEST_PRICE_TABLE = {
    "routine": 15000,
    "type": 75000,
    "special": 120000
}

TEST_RULES = {
    "power cable": ["routine", "type"],
    "switchgear panel": ["routine"],
    "transformer": ["routine", "type", "special"]
}

def calculate_pricing(final_tech_decision, quantity=10):
    sku_id = final_tech_decision["selected_sku"]
    sku_specs = final_tech_decision["sku_specs"]

    unit_price = SKU_PRICE_TABLE[sku_id]["unit_price"]
    uom = SKU_PRICE_TABLE[sku_id]["uom"]

    material_cost = unit_price * quantity

    applicable_tests = TEST_RULES.get(sku_specs["product_type"], [])
    testing_cost = sum(TEST_PRICE_TABLE[t] for t in applicable_tests)

    packing_cost = 0.02 * material_cost
    transport_cost = 0.03 * material_cost

    total_cost = (
        material_cost
        + testing_cost
        + packing_cost
        + transport_cost
    )

    return {
        "sku": sku_id,
        "quantity": quantity,
        "uom": uom,
        "material_cost": material_cost,
        "testing_cost": testing_cost,
        "packing_cost": packing_cost,
        "transport_cost": transport_cost,
        "total_cost": total_cost
    }