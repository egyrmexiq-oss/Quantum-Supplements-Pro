import streamlit as st
import google.generativeai as genai
from rules import SEGURIDAD_SUPLEMENTOS 

# ==========================================
# ⚙️ CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

# ==========================================
# 🎨 FUNCIÓN: ALERTA CUÁNTICA CON BOTÓN A ESPECIALISTAS
# ==========================================
def mostrar_alerta_riesgo(suplemento, condicion, especialidad):
    st.markdown(f"""
    <div style="border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px; background-color: rgba(255, 75, 75, 0.1); margin: 20px 0;">
        <h3 style="color: #FF4B4B; margin-top: 0;">🚨 NOTIFICACIÓN DE RIESGO BIO-SISTÉMICO</h3>
        <p style="color: white;">Contraindicación crítica: <b>{suplemento.upper()}</b> + <b>{condicion}</b>.</p>
        <p style="color: white;"><b>PASO SUGERIDO:</b> Derivación inmediata a <b>{especialidad}</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    # Aquí está la "ventanilla" o botón al portal de salud
    st.link_button(f"🔎 Ver Especialistas en {especialidad}", "https://quantum-health.streamlit.app")

# ==========================================
# 🔐 LOGIN Y ESTADO DE MEMORIA (EL CONTADOR)
# ==========================================
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] # Esto activa el "contador" de mensajes

if not st.session_state.usuario_activo:
    # ... (Mantener tu bloque de login igual)
    st.markdown("## 🔐 Quantum Supplements")
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        if c.strip() == "DEMO":
            st.session_state.usuario_activo = "Cliente Admin"
            st.rerun()
    st.stop()

# ==========================================
# 📊 BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/tu-usuario/tu-repo/main/logo_quantum.png") # Tu logo Q
    st.success(f"👤 {st.session_state.usuario_activo}")
    st.markdown(f"**Mensajes en sesión:** {len(st.session_state.messages)}") # El contador real
    st.markdown("---")
    nivel = st.radio("Nivel de Respuesta:", ["Básica", "Media", "Experta"])
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 💊 LÓGICA DEL CHAT Y SEGURIDAD
# ==========================================
st.title("💊 Quantum Supplements")

# Mostrar mensajes previos (El historial)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Escribe tu consulta...")

if user_input:
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 🛡️ VERIFICAR SEGURIDAD (rules.py)
    trigger_safety = False
    for sup_key, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup_key in user_input.lower():
            trigger_safety = True
            with st.chat_message("assistant"):
                st.warning(f"🛡️ **Protocolo de Validación: {sup_key.capitalize()}**")
                st.write(data["pregunta"])
                res = st.radio("¿Confirmas alguna condición?", ["No", "Sí"], key=f"sec_{sup_key}")
                if res == "Sí":
                    mostrar_alerta_riesgo(sup_key, data['alerta_si'], data['especialidad'])
            break

    # 🤖 RESPUESTA DE IA (Si no hay alerta bloqueante)
    if not trigger_safety:
        with st.chat_message("assistant"):
            respuesta_ia = f"Analizando {user_input} bajo nivel {nivel}..." # Aquí conectas tu genai
            st.markdown(respuesta_ia)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
        # --- CÓDIGO TEMPORAL DE DIAGNÓSTICO ---
#if st.button("🕵️ Ver Modelos Disponibles"):
    #try:
        #st.write("Consultando a Google...")
        #for m in genai.list_models():
            #if 'generateContent' in m.supported_generation_methods:
                #st.code(f"Nombre: {m.name}")
    #except Exception as e:
        #st.error(f"Error: {e}")