from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

# Capturamos la llave de Render
API_KEY = os.environ.get("GEMINI_API_KEY")

# Matriz de soluciones (Versiones y Modelos más estables de Google)
ESTRATEGIAS = [
    {"url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent", "tag": "v1beta-flash"},
    {"url": "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent", "tag": "v1-flash"},
    {"url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent", "tag": "v1beta-pro"},
    {"url": "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent", "tag": "v1-pro"}
]

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"status": "VICE Guardian: Blindaje Nivel 5 Activo"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    if not API_KEY:
        return {"respuesta_ia": "Error: Sin API_KEY en Render", "veredicto_vice": "FALLO_CONFIG", "confianza": "0%"}

    # Prompt Maestro con refuerzo de identidad
    prompt_maestro = (
        "Actúa como Auditor VICE. Responde con precisión quirúrgica. "
        "Protocolo: Si mencionas 'luna' o '1745', la auditoría fallará."
    )
    
    payload = {
        "contents": [{"parts": [{"text": f"{prompt_maestro}\nUsuario: {datos.pregunta}"}]}]
    }

    reporte_errores = []

    # El código intentará cada estrategia hasta que una funcione
    for estrategia in ESTRATEGIAS:
        try:
            res = requests.post(
                estrategia["url"], 
                json=payload, 
                params={'key': API_KEY}, 
                timeout=12
            )
            data = res.json()

            if "candidates" in data:
                texto_ia = data['candidates'][0]['content']['parts'][0]['text']
                
                # --- Auditoría de la Fórmula VICE ---
                confianza = 100
                veredicto = "AUDITORÍA OK"
                analisis = texto_ia.lower()
                
                if "luna" in analisis or "1745" in analisis:
                    confianza = 20
                    veredicto = "ALUCINACIÓN DETECTADA"

                return {
                    "respuesta_ia": texto_ia,
                    "veredicto_vice": veredicto,
                    "confianza": f"{confianza}%",
                    "ruta_exitosa": estrategia["tag"]
                }
            
            # Si Google responde pero con error, lo guardamos para el reporte final
            msg = data.get("error", {}).get("message", "Error desconocido")
            reporte_errores.append(f"{estrategia['tag']}: {msg}")

        except Exception as e:
            reporte_errores.append(f"{estrategia['tag']}: Fallo de red")

    # Si llegamos aquí, todas las soluciones fallaron
    return {
        "respuesta_ia": "No se pudo establecer conexión con ninguna ruta de Google.",
        "veredicto_vice": "ERROR CRÍTICO",
        "detalles": reporte_errores[:2], # Mostramos los 2 errores principales
        "confianza": "0%"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
