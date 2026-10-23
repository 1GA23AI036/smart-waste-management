"""
recommendations.py
------------------
Disposal recommendations, recycling instructions, and environmental tips
for each of the 6 waste categories.
"""

RECOMMENDATIONS = {
    "Plastic": {
        "disposal_method": "Recycling Bin (Blue)",
        "steps": [
            "Rinse the plastic item to remove any food residue or liquid.",
            "Check the resin code (1–7) stamped on the bottom of the item.",
            "Flatten bottles and containers to save space in the bin.",
            "Remove caps and lids separately — they may be a different plastic type.",
            "Place in the designated blue recycling bin or plastic collection point.",
        ],
        "recycling_instruction": (
            "Plastics labelled #1 (PET) and #2 (HDPE) are widely accepted at "
            "kerbside recycling. Plastics #3–7 may require drop-off at a specialist "
            "recycling facility. Never place single-use plastic bags in the bin — "
            "return them to supermarket collection points."
        ),
        "env_tip": (
            "Every tonne of recycled plastic saves approximately 5,774 kWh of energy "
            "— enough to power a home for six months. Carry a reusable bag to cut "
            "single-use plastic at the source."
        ),
        "fun_fact": "Only 9% of all plastic ever produced has been recycled.",
        "color": "#3B82F6",
        "icon": "🧴",
        "badge": "RECYCLABLE",
        "badge_color": "#DBEAFE",
        "badge_text_color": "#1D4ED8",
    },

    "Paper": {
        "disposal_method": "Paper / Cardboard Recycling Bin",
        "steps": [
            "Remove any plastic windows (e.g., from envelopes) before recycling.",
            "Flatten cardboard boxes to maximise bin space.",
            "Keep paper dry — wet paper degrades fibres and cannot be recycled.",
            "Shred sensitive documents before placing in the recycling bin.",
            "Bundle newspapers and magazines with twine if collecting separately.",
        ],
        "recycling_instruction": (
            "Clean paper and cardboard are among the most recyclable materials — "
            "paper can be recycled up to 7 times. Avoid recycling paper soiled with "
            "food grease (e.g., pizza boxes) or wax-coated paper; compost or bin those instead."
        ),
        "env_tip": (
            "Recycling one tonne of paper saves 17 trees, 7,000 gallons of water, "
            "and 380 gallons of oil. Go paperless where possible and print on both sides."
        ),
        "fun_fact": "Recycling paper uses 70% less energy than making it from raw wood pulp.",
        "color": "#F59E0B",
        "icon": "📄",
        "badge": "RECYCLABLE",
        "badge_color": "#FEF3C7",
        "badge_text_color": "#B45309",
    },

    "Metal": {
        "disposal_method": "Metal / Steel Recycling Bin",
        "steps": [
            "Rinse cans and tins to remove food residue.",
            "Do NOT crush aluminium cans — many sorting facilities require them intact.",
            "Remove paper labels if possible (not always necessary).",
            "Separate ferrous metals (steel, iron) from non-ferrous (aluminium, copper).",
            "Take large metal items (appliances, scrap metal) to a local recycling centre.",
        ],
        "recycling_instruction": (
            "Aluminium and steel are infinitely recyclable without loss of quality. "
            "Aluminium cans can be back on the shelf within 60 days. "
            "Aerosol cans are recyclable once fully empty — leave the cap off."
        ),
        "env_tip": (
            "Recycling aluminium uses 95% less energy than producing it from bauxite ore. "
            "A single recycled aluminium can saves enough energy to run a TV for three hours."
        ),
        "fun_fact": "Steel is the most recycled material in the world by weight.",
        "color": "#6B7280",
        "icon": "🔩",
        "badge": "RECYCLABLE",
        "badge_color": "#F3F4F6",
        "badge_text_color": "#374151",
    },

    "Glass": {
        "disposal_method": "Glass Bank / Glass Recycling Bin",
        "steps": [
            "Rinse glass bottles and jars thoroughly.",
            "Sort by colour if your local scheme requires it (clear, green, brown).",
            "Remove metal lids and recycle them separately with metals.",
            "Do NOT include broken glass, ceramics, Pyrex, or window glass — "
            "these have different melting points and contaminate the batch.",
            "Take to a bottle bank or kerbside glass collection box.",
        ],
        "recycling_instruction": (
            "Glass is 100% recyclable and can be recycled endlessly without any "
            "degradation in quality. Never put glass in general household recycling "
            "bins unless your council specifically allows it — it can damage sorting machinery."
        ),
        "env_tip": (
            "Recycling glass reduces related air pollution by 20% and water pollution by 50%. "
            "Buy products in glass containers and return/reuse them whenever possible."
        ),
        "fun_fact": "A glass bottle takes up to 1 million years to decompose in a landfill.",
        "color": "#06B6D4",
        "icon": "🍶",
        "badge": "RECYCLABLE",
        "badge_color": "#CFFAFE",
        "badge_text_color": "#0E7490",
    },

    "Organic": {
        "disposal_method": "Green / Compost Bin or Home Compost",
        "steps": [
            "Separate organic waste from plastics and packaging before disposing.",
            "Place fruit and vegetable peels, food scraps, and garden waste in the compost bin.",
            "Avoid putting meat, dairy, or oily foods in a home compost heap (use a food caddy instead).",
            "Layer 'greens' (food scraps) with 'browns' (dry leaves, cardboard) for best composting.",
            "Compost can be ready in 2–6 months and used to enrich garden soil.",
        ],
        "recycling_instruction": (
            "Organic waste in landfills produces methane, a greenhouse gas 25× more potent "
            "than CO₂. Composting diverts this waste into nutrient-rich fertiliser, "
            "closing the loop in the natural carbon cycle."
        ),
        "env_tip": (
            "Food waste accounts for ~8% of global greenhouse gas emissions. "
            "Plan your meals, store food correctly, and compost what you cannot eat "
            "to make a meaningful personal impact."
        ),
        "fun_fact": "Composting food scraps can reduce household waste by up to 30%.",
        "color": "#22C55E",
        "icon": "🍃",
        "badge": "COMPOSTABLE",
        "badge_color": "#DCFCE7",
        "badge_text_color": "#15803D",
    },

    "E-Waste": {
        "disposal_method": "Certified E-Waste Collection Centre",
        "steps": [
            "Back up and wipe all personal data from devices before disposal.",
            "Never throw electronics in general household bins — toxic materials can leach into soil.",
            "Find your nearest certified e-waste recycler or manufacturer take-back programme.",
            "Remove batteries from devices and dispose of them at battery collection points.",
            "Consider donating working electronics to schools, charities, or repair cafés.",
        ],
        "recycling_instruction": (
            "E-waste contains valuable materials — gold, silver, copper, palladium — "
            "worth billions globally. It also contains hazardous substances (lead, mercury, "
            "cadmium) that require specialised processing. Always use a certified e-waste recycler."
        ),
        "env_tip": (
            "Global e-waste reached 62 million tonnes in 2022 — the equivalent of 1.5 million "
            "heavy trucks. Extend the life of your devices with repairs and upgrades before "
            "replacing them."
        ),
        "fun_fact": "One million recycled mobile phones yield ~35 lbs of gold, 770 lbs of silver, and 33 lbs of palladium.",
        "color": "#8B5CF6",
        "icon": "💻",
        "badge": "HAZARDOUS",
        "badge_color": "#EDE9FE",
        "badge_text_color": "#6D28D9",
    },
}


def get_recommendation(category: str) -> dict:
    """
    Return the full recommendation dict for a given waste category.

    Parameters
    ----------
    category : str
        One of: Plastic, Paper, Metal, Glass, Organic, E-Waste

    Returns
    -------
    dict with keys: disposal_method, steps, recycling_instruction,
                    env_tip, fun_fact, color, icon, badge, etc.
    """
    return RECOMMENDATIONS.get(category, RECOMMENDATIONS["Plastic"])


def get_all_categories() -> list:
    """Return list of all waste category names."""
    return list(RECOMMENDATIONS.keys())


# Quick-reference disposal methods (used in dashboard cards)
QUICK_DISPOSAL = {
    cat: data["disposal_method"] for cat, data in RECOMMENDATIONS.items()
}

# Environmental impact statistics for the dashboard
ENV_STATS = {
    "trees_saved":       {"value": 0,  "unit": "Trees Saved",       "icon": "🌳"},
    "co2_reduced":       {"value": 0,  "unit": "kg CO₂ Reduced",    "icon": "💨"},
    "energy_saved":      {"value": 0,  "unit": "kWh Energy Saved",  "icon": "⚡"},
    "water_saved":       {"value": 0,  "unit": "Litres Water Saved","icon": "💧"},
}

# Per-item environmental savings estimates (rough averages)
ITEM_SAVINGS = {
    "Plastic":  {"co2": 1.5,  "energy": 5.8,  "water": 10,   "trees": 0},
    "Paper":    {"co2": 0.9,  "energy": 4.1,  "water": 26,   "trees": 0.02},
    "Metal":    {"co2": 2.0,  "energy": 14.0, "water": 5,    "trees": 0},
    "Glass":    {"co2": 0.3,  "energy": 0.7,  "water": 1.5,  "trees": 0},
    "Organic":  {"co2": 0.5,  "energy": 0.2,  "water": 0,    "trees": 0},
    "E-Waste":  {"co2": 3.0,  "energy": 20.0, "water": 0,    "trees": 0},
}


def calculate_env_impact(history: list) -> dict:
    """
    Calculate cumulative environmental savings from a list of
    classified waste items.

    Parameters
    ----------
    history : list of dicts, each with key 'category'

    Returns
    -------
    dict with co2, energy, water, trees totals
    """
    totals = {"co2": 0.0, "energy": 0.0, "water": 0.0, "trees": 0.0}
    for item in history:
        cat = item.get("category", "Plastic")
        savings = ITEM_SAVINGS.get(cat, ITEM_SAVINGS["Plastic"])
        for k in totals:
            totals[k] += savings[k]

    return {
        "co2_reduced":   round(totals["co2"],    2),
        "energy_saved":  round(totals["energy"], 2),
        "water_saved":   round(totals["water"],  1),
        "trees_saved":   round(totals["trees"],  3),
    }
