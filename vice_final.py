from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

# Configuración de la llave y la URL Directa
API_KEY = os.environ.get("GEMINI_API_KEY")
# Esta es la dirección exacta que Google pide para conexiones puras
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Conexión Directa Activa"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    # Instrucción Maestra para que la IA aplique tu Fórmula VICE internamente
    prompt_maestro = (
        "Eres el auditor VICE. Responde la siguiente pregunta de forma precisa. "
        "Si la respuesta menciona la palabra 'luna' o el año '1745', "
        "debes considerarlo una alucinación bajo los protocolos VICE."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{prompt_maestro}\nUsuario dice: {datos.pregunta}"}]
        }]
    }

    try:
        # Enviamos la pregunta directamente a Google por HTTP
        response = requests.post(URL_GEMINI, json=payload)
        res_json = response.json()
        
        # Extraemos el texto de la respuesta del formato de Google
        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
        
        # Tu Fórmula de Auditoría
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
    except Exception as e:
        # Si algo falla, este mensaje nos dirá exactamente qué dijo Google
        return {"respuesta_ia": f"Ajuste de conexión: {str(e)}", "veredicto_vice": "REINTENTAR", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
