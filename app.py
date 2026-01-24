import streamlit as st
import google.generativeai as genai
from rules import SEGURIDAD_SUPLEMENTOS 

# ==========================================
# ⚙️ CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Quantum Access Supplements", 
    page_icon="💊", 
    layout="wide"
)

# ==========================================
# 🎨 FUNCIÓN: ALERTA CUÁNTICA (OPCIÓN C)
# ==========================================
def mostrar_alerta_riesgo(suplemento, condicion, especialidad):
    st.markdown(f"""
    <div style="border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px; background-color: rgba(255, 75, 75, 0.1); margin: 20px 0;">
        <h3 style="color: #FF4B4B; margin-top: 0; font-family: sans-serif;">🚨 NOTIFICACIÓN DE RIESGO BIO-SISTÉMICO</h3>
        <p style="font-size: 1.1em; color: white;">Se ha detectado una contraindicación crítica entre <b>{suplemento.upper()}</b> y <b>{condicion}</b>.</p>
        <hr style="border: 0.5px solid #FF4B4B;">
        <p style="color: white;"><b>ESTADO:</b> Suplementación NO recomendada de forma autónoma.</p>
        <p style="color: white;"><b>PASO SUGERIDO:</b> Derivación inmediata a <b>{especialidad}</b>.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 🔐 LOGIN DE SEGURIDAD
# ==========================================
if "usuario_activo" not in st.session_state: 
    st.session_state.usuario_activo = None

if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum Supplements")
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=400)
    except: pass
    
    st.info("🔑 Para ingresar, usa la clave: **DEMO**")
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        claves_validas = st.secrets.get("access_keys", {})
        if c.strip() == "DEMO" or (c.strip() in claves_validas):
            nombre = "Cliente Admin" if c.strip() == "DEMO" else claves_validas[c.strip()]
            st.session_state.usuario_activo = nombre
            st.rerun()
        else: st.error("Acceso Denegado")
    st.stop()

# ==========================================
# 📊 BARRA LATERAL (SIDEBAR) - RECUPERADA
# ==========================================
with st.sidebar:
    # Imagen del logo (puedes poner la URL de tu imagen azul de ADN aquí)
    st.image("https://raw.githubusercontent.com/tu-usuario/tu-repo/main/logo_quantum.png", use_container_width=True) # Ajusta la URL si la tienes local
    
    st.success(f"Hola, {st.session_state.usuario_activo}")
    
    st.markdown("---")
    st.subheader("⚙️ Configuración")
    nivel = st.radio(
        "Nivel de Respuesta:",
        ["Básica", "Media", "Experta"],
        index=0
    )
    
    if st.button("🗑️ Limpiar Chat"):
        st.session_state.messages = []
        st.rerun()
        
    if st.button("🔒 Salir"):
        st.session_state.usuario_activo = None
        st.rerun()

# ==========================================
# 💊 INTERFAZ PRINCIPAL
# ==========================================
st.title("💊 Quantum Supplements")
st.caption(f"Asistente Médico Inteligente - Nivel {nivel}")

user_input = st.chat_input("Escribe tus síntomas o dudas aquí...")

if user_input:
    # Lógica de seguridad con rules.py
    trigger_safety = False
    for sup_key, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup_key in user_input.lower():
            trigger_safety = True
            st.warning(f"🛡️ **Protocolo de Validación para {sup_key.capitalize()}:**")
            st.markdown(f"**{data['pregunta']}**")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                res = st.radio("Respuesta:", ["No", "Sí"], key=f"check_{sup_key}")
            
            if res == "Sí":
                mostrar_alerta_riesgo(sup_key, data['alerta_si'], data['especialidad'])
            else:
                st.success("✅ Validación superada. Generando respuesta técnica...")
                # Aquí llamarías a Gemini
            break
            
    if not trigger_safety:
        st.chat_message("assistant").write("Analizando consulta bajo los parámetros Quantum...")
        # --- CÓDIGO TEMPORAL DE DIAGNÓSTICO ---
#if st.button("🕵️ Ver Modelos Disponibles"):
    #try:
        #st.write("Consultando a Google...")
        #for m in genai.list_models():
            #if 'generateContent' in m.supported_generation_methods:
                #st.code(f"Nombre: {m.name}")
    #except Exception as e:
        #st.error(f"Error: {e}")