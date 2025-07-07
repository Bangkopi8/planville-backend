
INTENTS = {
    "beratung": {
        "keywords": ["beratung", "termin", "kostenfrei", "kostenlose", "berater", "beratungstermin"],
        "response_type": "booking"
    },
    "preis": {
        "keywords": ["preis", "kosten", "angebot", "paket", "berechnung", "schätzung", "estimasi"],
        "response_type": "price_info"
    },
    "technik": {
        "keywords": ["pv", "photovoltaik", "solaranlage", "speicher", "leistung", "wechselrichter", "montage"],
        "response_type": "technical_info"
    },
    "dokumente": {
        "keywords": ["unterlagen", "förderung", "zuschuss", "fördermittel", "dokumen", "izin", "formulir"],
        "response_type": "document_info"
    },
    "projekte": {
        "keywords": ["projekt", "zeitplan", "dauer", "fertigstellung", "progress", "pemasangan"],
        "response_type": "timeline"
    },
    "fallback": {
        "keywords": [],
        "response_type": "fallback"
    }
}

def detect_intent(message: str):
    message = message.lower()
    for intent, data in INTENTS.items():
        for keyword in data["keywords"]:
            if keyword in message:
                return intent, data["response_type"]
    return "fallback", "fallback"

# Contoh:
# detect_intent("Wie teuer ist eine PV-Anlage mit Speicher?")
