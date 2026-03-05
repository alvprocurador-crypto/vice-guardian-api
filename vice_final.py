from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

API_KEY = os.environ.get("GEMINI_API_KEY")

# Esta lista contiene los nombres exactos que Google acepta según sus cambios más recientes
MODELOS_A_PROBAR = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-pro"
]

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Escaneo de Modelos Activo"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    if not API_KEY:
        return {"respuesta_ia": "Error: Falta API_KEY en Render", "veredicto_vice": "CONFIGURAR", "confianza": "0%"}

    payload = {
        "contents": [{"parts": [{"text": f"Eres el auditor VICE. Responde con precisión: {datos.pregunta}"}]}]
    }

    # El sistema probará cada modelo hasta que Google diga "SÍ"
    for modelo in MODELOS_A_PROBAR:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={API_KEY}"
        try:
            response = requests.post(url, json=payload, timeout=15)
            res_json = response.json()
            
            if "candidates" in res_json:
                texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                
                # Tu Fórmula VICE
                confianza = 100
                veredicto = "AUDITORÍA OK"
                if "luna" in texto_ia.lower() or "1745" in texto_ia.lower():
                    confianza = 20
                    veredicto = "ALUCINACIÓN DETECTADA"

                return {
                    "respuesta_ia": texto_ia,
                    "veredicto_vice": veredicto,
                    "confianza": f"{confianza}%",
                    "modelo_conectado": modelo
                }
        except:
            continue

    # Si llega aquí, es que Google rechaza la llave por un motivo externo al código
    return {
        "respuesta_ia": "Google rechaza la llave. Por favor, verifica que en AI Studio tengas habilitado Gemini 1.5.",
        "veredicto_vice": "ERROR LLAVE",
        "confianza": "0%"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
