from fastapi import FastAPI
import uvicorn
import os
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

# Configuración de la llave API
llave = os.environ.get("GEMINI_API_KEY")
if llave:
    genai.configure(api_key=llave)

# ESTE ES EL NOMBRE CORRECTO SEGÚN EL ERROR:
model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"mensaje": "VICE Guardian Operativo"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    try:
        # Forzamos el uso de la versión estable que Google pide
        response = model.generate_content(datos.pregunta)
        texto = response.text if response else "Sin respuesta."
        
        # Fórmula Vice
        confianza = 100
        veredicto = "AUDITORÍA OK"
        if "luna" in texto.lower() or "1745" in texto.lower():
            confianza = 20
            veredicto = "ALUCINACIÓN DETECTADA"

        return {
            "respuesta_ia": texto,
            "veredicto_vice": veredicto,
            "confianza": f"{confianza}%"
        }
    except Exception as e:
        # Este mensaje nos dirá si falta algo más
        return {"respuesta_ia": f"Ajuste necesario: {str(e)}", "veredicto_vice": "REINTENTAR", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
