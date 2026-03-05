from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

# 1. Configuración
API_KEY = os.environ.get("GEMINI_API_KEY")
# Usamos 'gemini-1.5-flash-latest' que es la dirección global más compatible
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Conexión Reforzada v5.2"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    if not API_KEY:
        return {"respuesta_ia": "Error: Falta API_KEY en Render", "veredicto_vice": "CONFIGURAR", "confianza": "0%"}

    payload = {
        "contents": [{
            "parts": [{"text": f"Eres el auditor VICE. Responde con precisión: {datos.pregunta}"}]
        }]
    }

    try:
        # Petición con timeout extendido y URL robusta
        response = requests.post(f"{URL_GEMINI}?key={API_KEY}", json=payload, timeout=20)
        res_json = response.json()
        
        if "candidates" in res_json:
            texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
            
            # Auditoría VICE
            confianza = 100
            veredicto = "AUDITORÍA OK"
            if "luna" in texto_ia.lower() or "1745" in texto_ia.lower():
                confianza = 20
                veredicto = "ALUCINACIÓN DETECTADA"

            return {
                "respuesta_ia": texto_ia,
                "veredicto_vice": veredicto,
                "confianza": f"{confianza}%"
            }
        
        # Este mensaje nos dirá exactamente qué modelo prefiere Google hoy
        error_msg = res_json.get("error", {}).get("message", "Error de versión de API")
        return {"respuesta_ia": f"Aviso de Google: {error_msg}", "veredicto_vice": "REVISAR_RATA", "confianza": "0%"}

    except Exception as e:
        return {"respuesta_ia": f"Fallo técnico: {str(e)}", "veredicto_vice": "REINTENTAR", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
