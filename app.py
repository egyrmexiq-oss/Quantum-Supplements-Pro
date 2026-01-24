import streamlit as st
import google.generativeai as genai
from rules import SEGURIDAD_SUPLEMENTOS 

# ⚙️ CONFIGURACIÓN
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

# 🎨 VENTANILLA DE ESPECIALISTAS
def mostrar_alerta_riesgo(suplemento, condicion, especialidad):
    with st.chat_message("assistant", avatar="🚨"):
        st.markdown(f"""
        <div style="border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px; background-color: rgba(255, 75, 75, 0.1); margin: 10px 0;">
            <h3 style="color: #FF4B4B; margin-top: 0;">🚨 RIESGO BIO-SISTÉMICO DETECTADO</h3>
            <p style="color: white;">Contraindicación: <b>{suplemento.upper()}</b> + <b>{condicion}</b>.</p>
            <hr style="border: 0.5px solid #FF4B4B;">
            <p style="color: white;"><b>ACCIÓN:</b> Consulta obligatoria con <b>{especialidad}</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        # Aquí la ventanilla física
        st.link_button(f"🔎 Contactar Especialista en {especialidad}", "https://quantum-health.streamlit.app")

# 🔐 LOGIN
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] 

if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum Supplements")
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        if c.strip().upper() == "DEMO":
            st.session_state.usuario_activo = "Visitante Temporal" # Cambiado de Admin a Visitante
            st.rerun()
    st.stop()

# 📊 SIDEBAR (CONTADOR REAL)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/tu-usuario/tu-repo/main/logo_quantum.png") # Tu logo
    st.success(f"👤 {st.session_state.usuario_activo}")
    
    # El contador ahora es reactivo a la lista de mensajes
    st.metric("Mensajes en sesión", len(st.session_state.messages))
    
    st.markdown("---")
    nivel = st.radio("Nivel de Respuesta:", ["Básica", "Media", "Experta"])
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.rerun()

# 💊 CHAT Y LÓGICA DE SEGURIDAD
st.title("💊 Quantum Supplements")

# Renderizar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Escribe tu consulta (ej: Magnesio)...")

if user_input:
    # 1. Registro inmediato en el contador
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Análisis de Seguridad
    trigger_safety = False
    for sup_key, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup_key in user_input.lower():
            trigger_safety = True
            with st.chat_message("assistant", avatar="🧬"):
                st.info(f"🛡️ **Protocolo Quantum: {sup_key.capitalize()}**")
                st.write(data["pregunta"])
                
                # Usamos un formulario para que la respuesta cuente y dispare la alerta
                with st.form(key=f"form_{sup_key}"):
                    opcion = st.radio("¿Padeces alguna de estas condiciones?", ["No", "Sí"])
                    enviar = st.form_submit_button("Validar Suplemento")
                    
                    if enviar:
                        if opcion == "Sí":
                            mostrar_alerta_riesgo(sup_key, data['alerta_si'], data['especialidad'])
                        else:
                            st.success("✅ Validación superada. Analizando dosis óptima...")
            break

    if not trigger_safety:
        with st.chat_message("assistant"):
            # Aquí va el motor de Gemini
            respuesta = f"Procesando info de {user_input} en nivel {nivel}..."
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
    
    # Forzar actualización del contador en la sidebar
    st.rerun()
        # --- CÓDIGO TEMPORAL DE DIAGNÓSTICO ---
#if st.button("🕵️ Ver Modelos Disponibles"):
    #try:
        #st.write("Consultando a Google...")
        #for m in genai.list_models():
            #if 'generateContent' in m.supported_generation_methods:
                #st.code(f"Nombre: {m.name}")
    #except Exception as e:
        #st.error(f"Error: {e}")