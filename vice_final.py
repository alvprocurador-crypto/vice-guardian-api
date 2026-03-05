from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

# 1. Configuración de la llave
API_KEY = os.environ.get("GEMINI_API_KEY")

# 2. LA RUTA EXACTA: Para Gemini 1.5 Flash, Google suele requerir v1beta
# Si esta falla, el reporte de error nos dirá el motivo de seguridad o cuota.
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Conexión Especial Activa"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    if not API_KEY:
        return {"respuesta_ia": "Error: API_KEY ausente en Render", "veredicto_vice": "REVISAR_ENV", "confianza": "0%"}

    prompt_maestro = (
        "Eres el auditor VICE. Responde de forma breve y precisa. "
        "Si mencionas 'luna' o '1745', el sistema detectará una alucinación."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{prompt_maestro}\nUsuario: {datos.pregunta}"}]
        }]
    }

    try:
        # Llamada directa con la URL de la versión beta (la más compatible con Flash)
        response = requests.post(f"{URL_GEMINI}?key={API_KEY}", json=payload, timeout=15)
        res_json = response.json()
        
        # Procesamiento de la respuesta
        if "candidates" in res_json:
            texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
            
            # Aplicación de Fórmula VICE
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
        
        # Si Google da un error, lo exponemos para saber qué falta
        error_msg = res_json.get("error", {}).get("message", "Error de modelo o versión")
        return {"respuesta_ia": f"Google informa: {error_msg}", "veredicto_vice": "REVISAR_GOOGLE", "confianza": "0%"}

    except Exception as e:
        return {"respuesta_ia": f"Excepción de red: {str(e)}", "veredicto_vice": "REINTENTAR", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
