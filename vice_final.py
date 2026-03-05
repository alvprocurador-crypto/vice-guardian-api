try:
        params = {'key': API_KEY}
        response = requests.post(URL_GEMINI, json=payload, params=params)
        res_json = response.json()
        
        # Validación: Si Google responde con error, mostrar el error real
        if "error" in res_json:
            return {
                "respuesta_ia": f"Error de Google: {res_json['error'].get('message', 'Desconocido')}",
                "veredicto_vice": "REVISAR API KEY",
                "confianza": "0%"
            }

        # Extraemos el texto solo si existe 'candidates'
        if 'candidates' in res_json:
            texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
            
            # Tu Fórmula de Auditoría VICE
            confianza = 100
            veredicto = "AUDITORÍA OK"
            if "luna" in texto_ia.lower() or "1745" in texto_ia.lower():
                confianza = 20
                veredicto = "ALUCINACIÓN DETECTADA"

            return {
                "respuesta_ia": texto_ia,
                "veredicto_vice": veredicto,
                "confianza": f"{confianza}%"
            }
        else:
            return {"respuesta_ia": "Google no envió candidatos. Revisa cuotas.", "veredicto_vice": "ERROR", "confianza": "0%"}

    except Exception as e:
        return {"respuesta_ia": f"Falla de red: {str(e)}", "veredicto_vice": "REINTENTAR", "confianza": "0%"}
