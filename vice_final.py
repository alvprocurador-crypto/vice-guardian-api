from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

API_KEY = os.environ.get("GEMINI_API_KEY")
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Conexión Directa Activa"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    if not API_KEY:
        return {"respuesta_ia": "Error: Falta API_KEY en Render", "veredicto_vice": "CONFIGURAR", "confianza": "0%"}

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
        # Petición a Google
        params = {'key': API_KEY}
        response = requests.post(URL_GEMINI, json=payload, params=params)
        res_json = response.json()
        
        # Validación de respuesta
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
        else:
            # Si Google responde pero no con texto (ej. error de clave)
            msg_error = res_json.get("error", {}).get("message", "Error desconocido")
            return {"respuesta_ia": f"Google dice: {msg_error}", "veredicto_vice": "REVISAR", "confianza": "0%"}

    except Exception as e:
        # Esta es la línea que causaba el error de sangría, ahora está alineada
        return {"respuesta_ia": f"Error de red: {str(e)}", "veredicto_vice": "REINTENTAR", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
