import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="CIRCE v2", page_icon="🩺", layout="centered")
st.title("🩺 CIRCE v2")
st.caption("Asistente con voz, razonamiento y primeros auxilios")

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")))

# --- REGISTRO DE EMERGENCIAS ---
if "emergencias" not in st.session_state:
    st.session_state.emergencias = {
        "911 Emergencias": "911",
        "Cruz Roja": "065",
        "Familiar 1": ""
    }

with st.sidebar:
    st.header("🚨 Mis números de emergencia")
    for nombre in list(st.session_state.emergencias.keys()):
        nuevo_num = st.text_input(nombre, value=st.session_state.emergencias[nombre], key=nombre)
        st.session_state.emergencias[nombre] = nuevo_num
        if nuevo_num:
            st.link_button(f"Llamar {nombre}", f"tel:{nuevo_num}")
    
    st.divider()
    st.header("📋 Procedimientos Rápidos")
    procedimiento = st.selectbox("Ver procedimiento:", 
        ["Seleccionar...", "RCP Adulto", "Maniobra de Heimlich", "Hemorragia", "Quemadura", "Convulsión", "Esguince"])
    
    if procedimiento != "Seleccionar...":
        guias = {
            "RCP Adulto": "1. Verificar si responde y respira\n2. Llamar 911\n3. 30 compresiones torácicas (5-6cm) en el centro del pecho\n4. 2 ventilaciones\n5. Repetir hasta que llegue ayuda.",
            "Maniobra de Heimlich": "1. Persona de pie, abrázala por detrás\n2. Puño sobre ombligo, otra mano encima\n3. Compresiones rápidas hacia adentro y arriba\n4. Si no expulsa, llamar 911.",
            "Hemorragia": "1. Presión directa con trapo limpio\n2. No quitar el primer trapo, poner otro encima\n3. Elevar extremidad si es posible\n4. Llamar 911 si no para en 10 min.",
            "Quemadura": "1. Enfriar con agua corriente 20 min (NO hielo, NO pasta)\n2. No reventar ampollas\n3. Cubrir con gasa limpia\n4. Si es grave/extensa, llamar 911.",
            "Convulsión": "1. No sujetar, no meter nada en la boca\n2. Poner de lado, quitar objetos peligrosos\n3. Cronometrar\n4. Llamar 911 si dura >5 min.",
            "Esguince": "Método RICE: Reposo, Hielo 15min, Compresión, Elevación."
        }
        st.info(guias[procedimiento])

# --- MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": """Eres CIRCE v2.
Personalidad: Empática, tranquila, clara, hablas en español mexicano sencillo.
Tarea: 1. Razona paso a paso (triaje). 2. Da primeros auxilios profesionales basados en guías de Cruz Roja/AHA. 3. Siempre di: Esto no es diagnóstico, acude a un médico. 4. Si es emergencia grave, di que llamen al 911 inmediatamente.
"""}]

# --- VOZ ---
audio_value = st.audio_input("🎤 Mantén presionado para hablar")
user_input = None
if audio_value:
    with st.spinner("Entendiendo tu voz..."):
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_value)
        user_input = transcription.text
        st.success(f"Dijiste: {user_input}")
else:
    user_input = st.chat_input("Escribe tu síntoma o emergencia