from fastapi import FastAPI
import uvicorn
import os
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

# Forzamos la configuración limpia de la API
llave = os.environ.get("GEMINI_API_KEY")
if llave:
    genai.configure(api_key=llave)

# Usamos el modelo base sin prefijos manuales, la librería se encarga
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
        # Usamos generate_content de la forma más sencilla y directa
        response = model.generate_content(datos.pregunta)
        
        if response and hasattr(response, 'text'):
            texto = response.text
        else:
            texto = "IA no devolvió texto. Revisa tu API Key."

        # Tu Fórmula Vice
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
        # Si falla, este mensaje nos dirá el error real de Google
        return {"respuesta_ia": f"Error de Google: {str(e)}", "veredicto_vice": "FALLO API", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
