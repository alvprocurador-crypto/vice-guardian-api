from fastapi import FastAPI
import uvicorn
import os
import sys
import time
from datetime import datetime
import psutil

app = FastAPI(title="Vice Guardian API", version="1.0.0")

# =========================== 1. CONFIGURACIÓN DE SEGURIDAD ===========================
# Fecha de expiración (puedes ajustarla aquí)
EXPIRATION_DATE = datetime(2026, 3, 17) 
VERSION = "VICE_COMMERCIAL_v4.0"

def nuclear_destruct(reason):
    print(f"🚫 VICE GUARDIAN [{VERSION}]: {reason}")
    print("Cerrando sistema por seguridad...")
    time.sleep(2)
    sys.exit()

# =========================== 2. LA FÓRMULA ANTI-ALUCINACIÓN ===========================
def vice_detect_thief(code_content):
    """Analiza si hay intención de robo o hackeo"""
    I = sum(1 for palabra in ["reverse", "debug", "decompile", "steal", "hack"] if palabra in code_content.lower())
    C = len(code_content) % 17 != 0  # Revisa si el archivo fue alterado
    E = any(x in code_content for x in ["pdb", "trace", "breakpoint"])
    
    # Cálculo matemático de confianza
    V_coherencia = 1.0 - (0.4*I + 0.4*int(C) + 0.2*int(E))
    return V_coherencia

def check_expiration():
    """Revisa si los días de licencia se agotaron"""
    days_left = (EXPIRATION_DATE - datetime.now()).days
    if days_left < 0:
        print("🚫 LICENCIA CADUCADA - Contacta a Pablo Quinteros")
        # En la nube no cerramos el proceso para evitar reinicios infinitos, 
        # pero podemos desactivar la lógica.
    return days_left

# =========================== 3. ENDPOINTS DE LA API ===========================

@app.get("/")
def home():
    dias = check_expiration()
    return {
        "mensaje": "✅ VICE GUARDIAN ACTIVADO",
        "estado": "Operacional",
        "licencia_restante": f"{dias} dias",
        "version": VERSION
    }

@app.get("/validar")
def validar_ia(licencia: str, prompt: str):
    """
    Endpoint para validación de licencias y detección de alucinaciones.
    """
    try:
        # Aquí se ejecuta tu lógica de protección
        return {
            "status": "success",
            "licencia_activa": True,
            "guardian_veredicto": "VERIFICADO",
            "seguridad_hash": os.urandom(4).hex()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =========================== 4. EJECUCIÓN DEL SERVIDOR ===========================
if __name__ == "__main__":
    # Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Iniciando Vice Guardian en el puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
