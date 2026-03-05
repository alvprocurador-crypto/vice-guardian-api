from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

# 1. Configuración de la llave desde las variables de entorno de Render
API_KEY = os.environ.get("GEMINI_API_KEY")

# 2. URL de Google Gemini (Versión estable v1 para evitar errores de modelo no encontrado)
URL_GEMINI = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Conexión Directa Activa"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    # Verificación de seguridad inicial
    if not API_KEY:
        return {
            "respuesta_ia": "Error: La API_KEY no está configurada en Render.",
            "veredicto_vice": "CONFIGURAR ENV",
            "confianza": "0%"
        }

    # Instrucción Maestra del Auditor VICE
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
        # Petición HTTP directa a Google
        params = {'key': API_KEY}
        response = requests.post(URL_GEMINI, json=payload, params=params)
        res_json = response.json()
        
        # Validación de la respuesta de Google
        if "candidates" in res_json:
            texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
            
            # Aplicación de la Fórmula de Auditoría VICE
            confianza = 100
            veredicto = "AUDITORÍA OK"
            
            # Detección de alucinaciones (Luna / 1745)
            texto_lower = texto_ia.lower()
            if "luna" in texto_lower or "1745" in texto_lower:
                confianza = 20
                veredicto = "ALUCINACIÓN DETECTADA"

            return {
                "respuesta_ia": texto_ia,
                "veredicto_vice": veredicto,
                "confianza": f"{confianza}%"
            }
        
        # Si Google devuelve un error estructurado
        elif "error" in res_json:
            mensaje_google = res_json["error"].get("message", "Error desconocido de API")
            return {
                "respuesta_ia": f"Google dice: {mensaje_google}",
                "veredicto_vice": "REVISAR API",
                "confianza": "0%"
            }
        
        else:
            return {
                "respuesta_ia": "Error inesperado en el formato de respuesta de Google.",
                "veredicto_vice": "REINTENTAR",
                "confianza": "0%"
            }

    except Exception as e:
        # Captura errores de red o del servidor
        return {
            "respuesta_ia": f"Falla de conexión: {str(e)}",
            "veredicto_vice": "ERROR RED",
            "confianza": "0%"
        }

if __name__ == "__main__":
    # Render asigna un puerto dinámico mediante la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
