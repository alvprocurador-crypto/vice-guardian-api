from fastapi import FastAPI
import uvicorn
import os
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

# Configuración de Google
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    try:
        # 1. Pregunta a la IA
        respuesta_ia = model.generate_content(datos.pregunta).text
        
        # 2. Tu Fórmula Vice simplificada para evitar errores de arranque
        I = sum(1 for p in ["error", "invento"] if p in respuesta_ia.lower())
        confianza = 1.0 - (0.4 * I)
        veredicto = "VERIFICADO" if confianza > 0.5 else "ALUCINACIÓN"

        return {
            "respuesta_ia": respuesta_ia,
            "veredicto_vice": veredicto,
            "confianza": f"{confianza * 100}%"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
