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

# CAMBIO CLAVE: Usamos 'gemini-1.5-pro' que es el más robusto y compatible
model = genai.GenerativeModel('gemini-1.5-pro')

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.get("/")
async def root():
    return {"mensaje": "Servidor VICE Guardian Activo"}

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    try:
        # Generación de contenido con el modelo Pro (Gratuito para desarrollo)
        response = model.generate_content(datos.pregunta)
        texto = response.text if response else "Sin respuesta del motor."
        
        # Tu Fórmula Vice (Veredicto y Confianza)
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
        return {"respuesta_ia": f"Error: {str(e)}", "veredicto_vice": "ERROR TECNICO", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
