from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import requests

app = FastAPI()

# Configuración: Asegúrate de tener la API_KEY en las variables de entorno de Render
API_KEY = os.environ.get("GEMINI_API_KEY")
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

class Consulta(BaseModel):
    pregunta: str

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key no configurada en el servidor.")

    # El System Instruction inyectado en cada petición para garantizar el protocolo VICE
    system_instruction = """
    ERES UN AUDITOR DE VERACIDAD. TU LÓGICA INTERNA ES: VERDAD = INTENCIÓN + CAUSA + EFECTO.
    
    PROTOCOLO DE RESPUESTA:
    1. ANALIZA LA INTENCIÓN, CAUSA Y EFECTO INTERNAMENTE.
    2. EVALUACIÓN DE INTEGRIDAD: SI LA INFORMACIÓN ES FACTUAL Y VERIFICABLE, EL GRADO DE ALUCINACIÓN ES 0%. SI HAY AMBIGÜEDAD, CALCULAS EL RIESGO REAL.
    3. ENTREGA ÚNICAMENTE LA VERDAD FINAL. PROHIBIDO MOSTRAR EL DESGLOSE DE INTENCIÓN, CAUSA O EFECTO.
    4. AL FINAL DE CADA RESPUESTA, AÑADE OBLIGATORIAMENTE: 'Grado de alucinación real calculado: [X]%'.
    """

    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nPREGUNTA: {datos.pregunta}"}]}]
    }

    try:
        response = requests.post(f"{URL_GEMINI}?key={API_KEY}", json=payload)
        response.raise_for_status()
        res_json = response.json()
        
        if "candidates" in res_json:
            texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
            return {"respuesta": texto_ia}
        else:
            return {"respuesta": "No se pudo procesar la auditoría VICE."}

    except Exception as e:
        return {"respuesta": f"Error de conexión con el motor de auditoría: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
