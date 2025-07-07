
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from rag_engine_v2 import answer_question
from intent_detection import detect_intent
from logger import get_logger
from faq_trigger import get_faq_answer
from lead_capture import capture_lead, capture_feedback

app = FastAPI()
logger = get_logger()

class ChatInput(BaseModel):
    message: str
    lang: str = "de"  # default bahasa: Jerman

@app.post("/chat")
async def chat(input_data: ChatInput) -> Dict:
    user_message = input_data.message
    user_lang = input_data.lang
    logger.info(f"User input: {user_message} | Lang: {user_lang}")

    # 0. Deteksi feedback
    feedback_keywords = {
        "de": ["danke", "hilfreich", "super", "top", "zufrieden"],
        "id": ["terima kasih", "membantu", "bagus", "oke", "mantap"]
    }
    for word in feedback_keywords.get(user_lang, []):
        if word in user_message.lower():
            capture_feedback(user_message, user_lang, "positif")
            return {"response": "Vielen Dank für Ihr Feedback! / Terima kasih atas tanggapannya!"}

    # 1. Coba cari jawaban di FAQ
    faq_response = get_faq_answer(user_message, user_lang)
    if faq_response:
        logger.info("Responded via FAQ")
        return {"response": faq_response}

    # 2. Intent detection
    intent, response_type = detect_intent(user_message)
    logger.info(f"Detected intent: {intent} | Response type: {response_type}")

    # 3. Simpan lead jika relevan
    if response_type in ["booking", "price_info"]:
        capture_lead(user_message, user_lang, response_type)

    # 4. Tentukan respons berdasarkan intent
    if response_type == "booking":
        response_text = "Gerne! Sie können einen kostenlosen Beratungstermin über unser Formular buchen: https://planville.de/kontakt"
    elif response_type == "price_info":
        response_text = "Unsere PV-Angebote hängen von Dachtyp, Region und Verbrauch ab. Möchten Sie eine individuelle Kalkulation?"
    elif response_type == "technical_info":
        response_text = answer_question(user_message)
    elif response_type == "document_info":
        response_text = "Für Fördermittel und Anträge unterstützen wir Sie gerne. Wünschen Sie Details zu Ihrem Bundesland?"
    elif response_type == "timeline":
        response_text = "Die Installation dauert ca. 6–8 Wochen nach Vertragsabschluss. Möchten Sie den genauen Ablauf erfahren?"
    else:
        # Fallback ke RAG
        response_text = answer_question(user_message)

    logger.info(f"Bot response: {response_text}")
    return {"response": response_text}
