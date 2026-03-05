from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()
API_KEY = os.environ.get("GEMINI_API_KEY")

# Lista de modelos por orden de prioridad
MODELOS = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro", "gemini-pro"]

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Blindaje Nivel 5 Activo"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    if not API_KEY:
        return {"respuesta_ia": "Error: Falta API_KEY en Render", "veredicto_vice": "CONFIGURAR", "confianza": "0%"}

    payload = {"contents": [{"parts": [{"text": f"Eres el auditor VICE. Responde: {datos.pregunta}"}]}]}
    
    # Intentamos cada modelo en la versión v1beta (la más flexible)
    for nombre_modelo in MODELOS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{nombre_modelo}:generateContent?key={API_KEY}"
        try:
            res = requests.post(url, json=payload, timeout=10)
            data = res.json()
            if "candidates" in data:
                texto = data['candidates'][0]['content']['parts'][0]['text']
                return {"respuesta_ia": texto, "veredicto_vice": "AUDITORÍA OK", "confianza": "100%", "modelo": nombre_modelo}
        except:
            continue

    # Si todo falla, le preguntamos a Google: ¿Qué modelos me dejas usar?
    try:
        diag = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}").json()
        modelos_vivos = [m["name"] for m in diag.get("models", [])]
        return {"respuesta_ia": f"Tu llave solo permite: {modelos_vivos}", "veredicto_vice": "ERROR PERMISOS", "confianza": "0%"}
    except:
        return {"respuesta_ia": "Error crítico de conexión regional.", "veredicto_vice": "CAMBIAR REGION", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
