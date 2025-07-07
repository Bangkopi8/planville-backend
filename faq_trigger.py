
# faq_trigger.py

faq_knowledge_base = {
    "kosten": {
        "de": "Unsere Beratung ist komplett kostenlos. Sie können jederzeit einen Termin buchen.",
        "id": "Konsultasi kami sepenuhnya gratis. Silakan jadwalkan janji kapan saja."
    },
    "garantie": {
        "de": "Unsere Photovoltaikanlagen haben eine Garantie von bis zu 25 Jahren.",
        "id": "Sistem PV kami memiliki garansi hingga 25 tahun."
    },
    "dauer": {
        "de": "Die Installation dauert in der Regel etwa 6 Wochen.",
        "id": "Proses instalasi biasanya memakan waktu sekitar 6 minggu."
    },
    "förderung": {
        "de": "Es gibt staatliche Förderungen für Solaranlagen. Wir helfen Ihnen gerne dabei.",
        "id": "Ada subsidi pemerintah untuk panel surya. Kami siap membantu prosesnya."
    }
}

def get_faq_answer(message: str, lang: str = "de") -> str | None:
    message = message.lower()
    for keyword, translations in faq_knowledge_base.items():
        if keyword in message:
            return translations.get(lang, translations["de"])
    return None
