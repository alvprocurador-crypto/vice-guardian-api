from fastapi import FastAPI
import uvicorn
import os
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

# Configuración simplificada de la llave
llave = os.environ.get("GEMINI_API_KEY")
if llave:
    genai.configure(api_key=llave)

model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    try:
        # Intentamos obtener respuesta
        response = model.generate_content(datos.pregunta)
        texto = response.text if response else "Sin respuesta del motor."
        
        # Fórmula Vice básica para evitar fallos de memoria
        confianza = 100
        if "luna" in texto.lower() or "1745" in texto.lower():
            confianza = 20
            veredicto = "ALUCINACIÓN DETECTADA"
        else:
            veredicto = "AUDITORÍA OK"

        return {
            "respuesta_ia": texto,
            "veredicto_vice": veredicto,
            "confianza": f"{confianza}%"
        }
    except Exception as e:
        return {"respuesta_ia": f"Error: {str(e)}", "veredicto_vice": "REVISAR CONEXIÓN", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
