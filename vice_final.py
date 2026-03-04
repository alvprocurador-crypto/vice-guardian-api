From fastapi import FastAPI
from pydantic import BaseModel
import os
import google.genai as genai  # Nueva librería oficial (2026)

app = FastAPI()

# Configuración robusta de la llave (para Render/GitHub)
llave = os.environ.get("GEMINI_API_KEY")
if not llave:
    raise RuntimeError("❌ FALTA GEMINI_API_KEY en variables de entorno")

client = genai.Client(api_key=llave)
modelo_id = "gemini-2.0-flash-exp"  # Modelo actualizado y rápido [web:13][web:18]

class Consulta(BaseModel):
    pregunta: str
    licencia: str  # Mantengo por si lo usas después

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    try:
        # Generación con nueva API (texto directo como contents)
        response = client.models.generate_content(
            model=modelo_id,
            contents=datos.pregunta,
        )
        texto = response.text if response and hasattr(response, 'text') else "Sin respuesta del modelo."
        
        # Tu fórmula VICE original (perfecta)
        confianza = 100
        if "luna" in texto.lower() or "1745" in texto.lower():
            confianza = 20
            veredicto = "ALUCINACIÓN DETECTADA"
        else:
            veredicto = "AUDITORÍA OK"

        return {
            "respuesta_ia": texto,
            "veredicto_vice": veredicto,
            "confianza": f"{confianza}%",
            "licencia_usada": datos.licencia  # Para logs futuros
        }
    except Exception as e:
        return {
            "respuesta_ia": f"Error: {str(e)}",
            "veredicto_vice": "REVISAR CONEXIÓN",
            "confianza": "0%",
            "licencia_usada": datos.licencia
        }

# Para probar docs en /docs (FastAPI automático)
@app.get("/")
async def root():
    return {"mensaje": "🛡️ VICE Guardian API lista", "endpoint": "/preguntar"}
