from fastapi import FastAPI
import uvicorn
import os
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

# Configuración de Google Gemini
# Asegúrate de tener la variable GEMINI_API_KEY en los Environment Variables de Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    pregunta: str
    licencia: str

@app.post("/preguntar")
async def chat_guardian(datos: Consulta):
    try:
        # 1. Intentamos obtener la respuesta de la IA
        response = model.generate_content(datos.pregunta)
        respuesta_ia = response.text if response and hasattr(response, 'text') else ""
        
        # 2. Si la respuesta viene vacía (el error "None" que tenías)
        if not respuesta_ia or respuesta_ia.strip() == "":
            return {
                "respuesta_ia": "El sistema detectó una alucinación crítica o bloqueo de seguridad.",
                "veredicto_vice": "RIESGO EXTREMO / ALUCINACIÓN",
                "confianza": "0%"
            }

        # 3. --- LA FÓRMULA VICE MEJORADA ---
        # Definimos palabras que indican que la IA está inventando o dudando
        palabras_alerta = ["luna", "1745", "error", "desconozco", "invento", "falso"]
        puntos_riesgo = sum(20 for palabra in palabras_alerta if palabra in respuesta_ia.lower())
        
        # Calculamos la confianza (Base 100%)
        confianza_num = 100 - puntos_riesgo
        if confianza_num < 0: confianza_num = 0
        
        # Determinamos el veredicto final
        if confianza_num >= 80:
            veredicto = "AUDITORÍA APROBADA (DATOS SEGUROS)"
        elif confianza_num >= 50:
            veredicto = "PRECAUCIÓN (POSIBLE INCOHERENCIA)"
        else:
            veredicto = "ALUCINACIÓN DETECTADA (NO CONFIABLE)"

        return {
            "respuesta_ia": respuesta_ia,
            "veredicto_vice": veredicto,
            "confianza": f"{confianza_num}%"
        }

    except Exception as e:
        # Si algo falla en el proceso, enviamos un mensaje de error claro
        return {
            "respuesta_ia": f"Error técnico en el motor Vice: {str(e)}",
            "veredicto_vice": "SISTEMA FUERA DE CONTROL",
            "confianza": "ERROR"
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
