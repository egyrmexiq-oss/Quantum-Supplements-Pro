import streamlit as st
import google.generativeai as genai
from rules import SEGURIDAD_SUPLEMENTOS # Conexión con tu nuevo cerebro

# ==========================================
# ⚙️ CONFIGURACIÓN DE PÁGINA (WIDE MODE)
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
    
    st.info(f"💡 Puedes encontrar especialistas certificados en **Quantum Health** para una valoración formal.")

# ==========================================
# 🔐 LOGIN DE SEGURIDAD
# ==========================================
if "usuario_activo" not in st.session_state: 
    st.session_state.usuario_activo = None

if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum Supplements")
    try: 
        st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=400)
    except: pass
    
    st.audio("https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3", loop=True, autoplay=True)
    st.info("🔑 Para ingresar, usa la clave: **DEMO**")
    
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        # Acepta DEMO o claves en secrets
        claves_validas = st.secrets.get("access_keys", {})
        if c.strip() == "DEMO" or (c.strip() in claves_validas):
            nombre = "Visitante" if c.strip() == "DEMO" else claves_validas[c.strip()]
            st.session_state.usuario_activo = nombre
            st.rerun()
        else: 
            st.error("Acceso Denegado")
    st.stop()

# ==========================================
# 💊 INTERFAZ PRINCIPAL - ASISTENTE CUÁNTICO
# ==========================================
st.title("💊 Quantum Supplements")
st.caption(f"Bienvenido, {st.session_state.usuario_activo} | Bio-Consultor de Inteligencia Artificial")

# Entrada del usuario
user_input = st.chat_input("Escribe tu duda sobre suplementos (ej: Magnesio, Zinc)...")

if user_input:
    # 1. BUSCAR COINCIDENCIAS EN LAS REGLAS DE SEGURIDAD
    trigger_safety = False
    input_lower = user_input.lower()
    
    for sup_key, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup_key in input_lower:
            trigger_safety = True
            st.warning(f"🛡️ **Análisis de Seguridad: {sup_key.capitalize()}**")
            st.markdown(f"**{data['pregunta']}**")
            
            # Selector de triaje
            col1, col2 = st.columns([1, 4])
            with col1:
                respuesta = st.radio("Respuesta:", ["No", "Sí"], key=f"radio_{sup_key}")
            
            if respuesta == "Sí":
                mostrar_alerta_riesgo(sup_key, data['alerta_si'], data['especialidad'])
            else:
                st.success("✅ Validación superada. Procesando información técnica con la IA...")
                # Aquí seguiría la lógica de Gemini (genai.generate_content)
                st.write("*(Simulación)*: El magnesio es seguro para ti. La dosis sugerida es...")
            break # Detenemos el ciclo si encontramos el suplemento
            
    # 2. SI NO HAY REGLAS ESPECÍFICAS, PROCESAR COMO CONSULTA GENERAL
    if not trigger_safety:
        with st.chat_message("assistant"):
            st.write("Analizando consulta general en el ecosistema Quantum...")
            # Aquí va tu código habitual de respuesta de Gemini
            st.info("La IA está procesando tu consulta de bienestar.")
        # --- CÓDIGO TEMPORAL DE DIAGNÓSTICO ---
#if st.button("🕵️ Ver Modelos Disponibles"):
    #try:
        #st.write("Consultando a Google...")
        #for m in genai.list_models():
            #if 'generateContent' in m.supported_generation_methods:
                #st.code(f"Nombre: {m.name}")
    #except Exception as e:
        #st.error(f"Error: {e}")