import streamlit as st
import google.generativeai as genai
import json
import os
from rules import SEGURIDAD_SUPLEMENTOS

# ==========================================
# 1. CONFIGURACIÓN Y ESTILO
# ==========================================
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

def inyectar_estilo_quantum():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {
            background-color: #0E1117;
            border-right: 1px solid #262730;
        }
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            color: #00FF94 !important;
            font-weight: 700;
        }
        button[kind="primary"] {
            background-color: #FF4B4B !important;
            border: none;
            transition: all 0.3s;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
        }
        </style>
        """, unsafe_allow_html=True)

inyectar_estilo_quantum()

# ==========================================
# 2. SISTEMA DE ESTADÍSTICAS
# ==========================================
FILE_STATS = "quantum_stats.json"

def gestionar_estadisticas(tipo="leer"):
    if not os.path.exists(FILE_STATS):
        with open(FILE_STATS, "w") as f:
            json.dump({"sesiones_totales": 0, "consultas_totales": 0}, f)
    
    with open(FILE_STATS, "r") as f:
        data = json.load(f)

    if tipo == "nueva_sesion":
        data["sesiones_totales"] += 1
    elif tipo == "nueva_consulta":
        data["consultas_totales"] += 1
    
    if tipo != "leer":
        with open(FILE_STATS, "w") as f:
            json.dump(data, f)
    return data

# ==========================================
# 3. CONEXIÓN GEMINI (MODELO 2.0)
# ==========================================
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash-exp') 
    else:
        st.error("⚠️ Error: Falta 'GEMINI_API_KEY' en secrets.toml")
        st.stop()
except Exception as e:
    st.error(f"Error Conexión: {e}")

# ==========================================
# 4. GESTIÓN DE MEMORIA
# ==========================================
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] 
if "alerta_fijada" not in st.session_state: st.session_state.alerta_fijada = None
if "validaciones_ok" not in st.session_state: st.session_state.validaciones_ok = set()

if "sesion_iniciada" not in st.session_state:
    gestionar_estadisticas("nueva_sesion")
    st.session_state.sesion_iniciada = True

# ==========================================
# 5. LOGIN
# ==========================================
if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum Supplements")
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=400)
    except: pass
    
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        claves = st.secrets.get("access_keys", {})
        if c.strip().upper() == "DEMO":
            st.session_state.usuario_activo = "Visitante Temporal"
            st.rerun()
        elif c in claves:
            st.session_state.usuario_activo = claves[c]
            st.rerun()
    st.stop()

# ==========================================
# 6. SIDEBAR
# ==========================================
stats = gestionar_estadisticas("leer")
with st.sidebar:
    st.success(f"👤 {st.session_state.usuario_activo}")
    c1, c2 = st.columns(2)
    c1.metric("Sesiones", stats["sesiones_totales"])
    c2.metric("Consultas", stats["consultas_totales"])
    
    st.markdown("---")
    nivel = st.radio("Nivel IA:", ["Básica", "Media", "Experta"])
    
    with st.expander("📂 Recursos"):
        st.link_button("📝 Alta", "https://forms.google.com/...") 
        st.link_button("📊 Datos", "https://docs.google.com/spreadsheets/...")
    
    if st.button("🗑️ Borrar"):
        st.session_state.messages = []
        st.session_state.alerta_fijada = None
        st.session_state.validaciones_ok = set()
        st.rerun()

# ==========================================
# 7. INTERFAZ PRINCIPAL
# ==========================================
st.title("💊 Quantum Supplements")

# Alerta Roja (Persistente)
if st.session_state.alerta_fijada:
    val = st.session_state.alerta_fijada
    st.markdown(f"""
    <div style="border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px; background-color: rgba(255, 75, 75, 0.1); margin-bottom: 20px;">
        <h3 style="color: #FF4B4B; margin: 0;">🚨 RIESGO DETECTADO</h3>
        <p style="color: white;">Conflicto: <b>{val['sup'].upper()}</b> + <b>{val['condicion']}</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button(f"🩺 Contactar {val['esp']}", "https://quantum-health.streamlit.app", type="primary")

# Portada


# Historial


# ==========================================
# 8. CEREBRO CUÁNTICO (LÓGICA CORREGIDA)
# ==========================================

# A. CAPTURA DE INPUT (Solo guarda y recarga)
if prompt := st.chat_input("Consulta sobre suplementos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    gestionar_estadisticas("nueva_consulta")
    st.rerun() # <--- CLAVE: Recargamos para procesar el mensaje desde el historial

# B. PROCESAMIENTO (Lee del historial, NO del input)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    
    # Recuperamos el último mensaje del usuario
    last_msg = st.session_state.messages[-1]["content"]
    stop_processing = False
    
    # 1. VERIFICACIÓN DE SEGURIDAD
    for sup, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup in last_msg.lower():
            
            # Caso 1: Si ya hay alerta activa por esto, NO contestamos
            if st.session_state.alerta_fijada and st.session_state.alerta_fijada['sup'] == sup:
                stop_processing = True
                break
                
            # Caso 2: Si ya fue validado ("Estoy sano"), lo ignoramos y seguimos
            if sup in st.session_state.validaciones_ok:
                continue 
            
            # Caso 3: Nueva detección -> Preguntamos
            with st.chat_message("assistant", avatar="🛡️"):
                st.warning(f"**Protocolo de Seguridad: {sup.capitalize()}**")
                st.write(data["pregunta"])
                
                c1, c2 = st.columns(2)
                if c1.button("No, estoy sano"):
                    st.session_state.validaciones_ok.add(sup)
                    st.rerun() # Al recargar, entrará en el Caso 2
                
                if c2.button("Sí, tengo esa condición"):
                    st.session_state.alerta_fijada = {
                        "sup": sup,
                        "condicion": data["alerta_si"],
                        "esp": data["especialidad"]
                    }
                    st.rerun() # Al recargar, entrará en el Caso 1
            
            st.stop() # Detenemos todo mientras esperamos el clic
            
    # 2. GENERACIÓN DE RESPUESTA (Solo si no hay bloqueos)
    if not stop_processing:
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analizando con Gemini 2.0..."):
                try:
                    prompt_ia = f"""
                    Actúa como Experto en Suplementos. Nivel: {nivel}.
                    Usuario pregunta: "{last_msg}".
                    Responde con estructura: Beneficio 🧬, Dosis 💊, Precaución ⚠️.
                    """
                    response = model.generate_content(prompt_ia)
                    res_text = response.text
                    
                    st.markdown(res_text)
                    st.session_state.messages.append({"role": "assistant", "content": res_text})
                    # Ya no hacemos rerun aquí para que no parpadee
                    
                except Exception as e:
                    st.error(f"⚠️ Error IA: {str(e)}")
                    st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})


        # --- CÓDIGO TEMPORAL DE DIAGNÓSTICO ---
#if st.button("🕵️ Ver Modelos Disponibles"):
    #try:
        #st.write("Consultando a Google...")
        #for m in genai.list_models():
            #if 'generateContent' in m.supported_generation_methods:
                #st.code(f"Nombre: {m.name}")
    #except Exception as e:
        #st.error(f"Error: {e}")