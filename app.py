import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="CIRCE v2 - Voz", page_icon="🎙️", layout="centered")

st.title("CIRCE v2 - Asistente de Enfermeria")
st.write("Habla o escribe, te escucho y te respondo con voz.")

api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not api_key:
    st.error("Falta la OPENAI_API_KEY en Secrets")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres CIRCE v2, asistente de enfermeria experto. Respondes en espanol, claro, paso a paso. Das procedimientos, emergencias, medicamentos. Si hay riesgo vital, indica ir a urgencias."}
    ]

for m in st.session_state.messages[1:]:
    with st.chat_message(m["role"]):
        st.write(m["content"])

user_input = st.chat_input("Escribe aqui tu pregunta")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.write(answer)

            # Voz
            try:
                speech = client.audio.speech.create(
                    model="tts-1",
                    voice="nova",
                    input=answer[:4000]
                )
                st.audio(speech.content, format="audio/mp3")
            except Exception as e:
                st.warning(f"No se pudo generar audio: {e}")

            st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()
st.caption("CIRCE v2 | Hecho para ti")