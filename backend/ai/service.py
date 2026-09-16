import time
import uuid

import requests
from sqlalchemy.orm import Session

from backend.ai import repository as ai_repository
from backend.ai.schemas import SmartTaskExtraction
from backend.core.config import get_settings

settings = get_settings()

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.6-flash:generateContent"
)


class AIServiceError(Exception):
    pass


def _call_gemini(prompt: str) -> str:
    response = requests.post(
        f"{GEMINI_URL}?key={settings.gemini_api_key}",
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"},
        },
        timeout=45,
    )

    if response.status_code != 200:
        raise AIServiceError(f"Gemini API error: {response.status_code} - {response.text}")

    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise AIServiceError(f"Unexpected Gemini response format: {data}") from exc


def extract_task_from_text(
    db: Session, organization_id: uuid.UUID, user_id: uuid.UUID, text: str
) -> SmartTaskExtraction:
    prompt = f"""Eres un asistente que convierte solicitudes en lenguaje natural en tareas estructuradas para un sistema de gestión empresarial.

Analiza el siguiente texto y responde ÚNICAMENTE con un JSON válido (sin texto adicional, sin markdown) con esta estructura exacta:
{{
  "title": "un título corto y claro para la tarea (máximo 80 caracteres)",
  "priority": "debe ser exactamente uno de: low, medium, high, urgent",
  "due_date_hint": "si el texto menciona una fecha o urgencia temporal, descríbela brevemente en texto (ej: 'mañana', 'la próxima semana'), o null si no se menciona",
  "reasoning": "una frase corta explicando por qué elegiste esa prioridad"
}}

Texto a analizar: "{text}"
"""

    start = time.perf_counter()
    raw_response = _call_gemini(prompt)
    latency_ms = int((time.perf_counter() - start) * 1000)

    import json

    try:
        parsed = json.loads(raw_response)
        extraction = SmartTaskExtraction(**parsed)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise AIServiceError(f"Could not parse AI response as valid extraction: {raw_response}") from exc

    ai_repository.log_request(
        db,
        organization_id=organization_id,
        user_id=user_id,
        module="extraction",
        prompt=text,
        response=parsed,
        latency_ms=latency_ms,
    )

    return extraction