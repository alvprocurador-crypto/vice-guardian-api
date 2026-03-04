from fastapi import FastAPI
import uvicorn
import os
import sys
import time
from datetime import datetime
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI(title="Vice Guardian AI", version="1.0.0")

# =========================== 1. CONFIGURACIÓN DE SEGURIDAD ===========================
# Mantenemos tus parámetros originales
EXPIRATION_DATE = datetime(2026, 3, 17) 
VERSION = "VICE_COMMERCIAL_AI_v5.0"

# Configuramos la Inteligencia de Google usando la llave que guardaste en Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    pregunta: str
    licencia: str

# =========================== 2. TU FÓRMULA VICE (PROTEGIDA) ===========================
def vice_detect_logic(text_content):
    """
    Tu fórmula original adaptada para analizar la respuesta de la IA.
    """
    # Analiza si la respuesta de la IA contiene palabras sospechosas de error
    I = sum(1 for palabra in ["error", "unknown", "failed", "inconsistent"] if palabra in text_content.lower())
    C = len(text_content) % 17 != 0  # Tu validación matemática original
    E = any(x in text_content for x in ["invento", "alucinacion", "no lo se"])
    
    # Tu Cálculo matemático de confianza original
    V_coherencia = 1.0 - (0.4*I + 0.4*int(C) + 0.2*int(E))
    return V_coherencia

def check_expiration():
    """Revisa si los días de licencia se agotaron"""
    days_left = (EXPIRATION_DATE - datetime.now()).days
    return days_left

# =========================== 3. EL NUEVO CEREBRO (CHAT + AUDITORÍA) ===========================

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    """
    Este es el motor principal: Pregunta a Google -> Pasa por tu Fórmula -> Responde al .exe
    """
    dias = check_expiration()
    if dias < 0:
        return {"error": "LICENCIA CADUCADA", "contacto": "Pablo Quinteros"}

    try:
        # 1. El servidor le pregunta a la IA de Google
        chat_session = model.generate_content(datos.pregunta)
        respuesta_ia = chat_session.text

        # 2. Aplicamos TU FÓRMULA VICE a lo que dijo Google
        nivel_confianza = vice_detect_logic(respuesta_ia)
        
        veredicto = "VERIFICADO" if nivel_confianza > 0.5 else "ALUCINACIÓN DETECTADA"

        # 3. Enviamos todo de vuelta a tu ventana negra
        return {
            "respuesta_ia": respuesta_ia,
            "veredicto_vice": veredicto,
            "confianza": f"{nivel_confianza * 100:.2f}%",
            "version": VERSION,
            "seguridad_hash": os.urandom(4).hex()
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    dias = check_expiration()
    return {
        "mensaje": "✅ VICE GUARDIAN AI ACTIVADO",
        "licencia_restante": f"{dias} dias",
        "google_api": "CONECTADA" if os.environ.get("GEMINI_API_KEY") else "ERROR"
    }

# =========================== 4. EJECUCIÓN DEL SERVIDOR ===========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
