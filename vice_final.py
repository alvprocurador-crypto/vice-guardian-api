from fastapi import FastAPI
import uvicorn
import os
import requests
from pydantic import BaseModel

app = FastAPI()

API_KEY = os.environ.get("GEMINI_API_KEY")
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    # La Fórmula VICE integrada como instrucción de arquitectura de pensamiento
    formula_vice_prompt = f"""
    Eres el Auditor VICE. Tu única misión es la veracidad absoluta.
    Consulta: {datos.pregunta}
    
    PROTOCOLO DE RESPUESTA:
    1. Analiza los hechos y responde con 0% de alucinación.
    2. Si no existe una certeza absoluta, no inventes, indícalo.
    3. Al finalizar, realiza un 'Auditoría VICE': 
       - Si detectas cualquier mínima posibilidad de error o dato no verificado, 
         asigna CONFIANZA: 20%.
       - Si la respuesta está 100% verificada, asigna CONFIANZA: 100%.
    """

    payload = {"contents": [{"parts": [{"text": formula_vice_prompt}]}]}

    try:
        response = requests.post(f"{URL_GEMINI}?key={API_KEY}", json=payload, timeout=20)
        res_json = response.json()
        
        # Gestión de cuota
        if "error" in res_json and "quota" in str(res_json).lower():
            return {"respuesta_ia": "Límite de cuota alcanzado. Reinicio de sistema pendiente.", "veredicto_vice": "CUOTA_AGOTADA", "confianza": "0%"}

        if "candidates" in res_json:
            texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
            return {
                "respuesta_ia": texto_ia,
                "veredicto_vice": "AUDITORÍA VICE: PROCESADO",
                "confianza": "Verificar veredicto en respuesta_ia"
            }
            
        return {"respuesta_ia": "Error en el motor VICE", "veredicto_vice": "FALLO_MOTOR", "confianza": "0%"}

    except Exception as e:
        return {"respuesta_ia": f"Fallo crítico en Auditoría: {str(e)}", "veredicto_vice": "FALLO_SISTEMA", "confianza": "0%"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
