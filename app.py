import streamlit as st
import google.generativeai as genai
from rules import SEGURIDAD_SUPLEMENTOS 

# ==========================================
# ⚙️ CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

# ==========================================
# 🎨 FUNCIÓN: ALERTA CUÁNTICA
# ==========================================
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
        st.link_button(f"🔎 Contactar Especialista en {especialidad}", "https://quantum-health.streamlit.app")

# ==========================================
# 🔐 LOGIN Y ESTADO
# ==========================================
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] 

if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum Supplements")
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=400)
    except: pass
    st.audio("https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3", loop=True)
    
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        if c.strip().upper() == "DEMO":
            st.session_state.usuario_activo = "Visitante Temporal"
            st.rerun()
    st.stop()

# ==========================================
# 📊 BARRA LATERAL (SIDEBAR) - UNIFICADA
# ==========================================
with st.sidebar:
    # Eliminamos el texto suelto que generaba el cero extra
    st.success(f"👤 {st.session_state.usuario_activo}")
    st.metric("Mensajes en sesión", len(st.session_state.messages))
    
    st.markdown("---")
    nivel = st.radio("Nivel de Respuesta:", ["Básica", "Media", "Experta"])
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.rerun()
    if st.button("🔒 Salir"):
        st.session_state.usuario_activo = None
        st.rerun()

# ==========================================
# 💊 PORTADA Y CHAT
# ==========================================
# Si no hay mensajes, mostramos la portada elegante
if not st.session_state.messages:
    st.title("💊 Quantum Supplements")
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=300)
    except: pass
    st.info("Bienvenido al Bio-Consultor. Escribe el nombre de un suplemento para comenzar el análisis.")

# Renderizar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Escribe tu consulta (ej: Magnesio)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun() # Forzamos recarga para que el historial se vea arriba del input

# Lógica de procesamiento (solo si hay mensajes nuevos)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]["content"].lower()
    
    trigger_safety = False
    for sup_key, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup_key in last_msg:
            trigger_safety = True
            with st.chat_message("assistant", avatar="🧬"):
                st.warning(f"🛡️ **Protocolo Quantum: {sup_key.capitalize()}**")
                st.write(data["pregunta"])
                
                with st.form(key=f"form_{sup_key}"):
                    opcion = st.radio("¿Padeces alguna de estas condiciones?", ["No", "Sí"])
                    if st.form_submit_button("Validar Suplemento"):
                        if opcion == "Sí":
                            mostrar_alerta_riesgo(sup_key, data['alerta_si'], data['especialidad'])
                        else:
                            st.success("✅ Validación superada.")
            break

    if not trigger_safety:
        with st.chat_message("assistant"):
            respuesta = f"Analizando {last_msg} en nivel {nivel}. (Conexión con IA activa)"
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            st.rerun()
    
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