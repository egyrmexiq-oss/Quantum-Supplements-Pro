import streamlit as st
import google.generativeai as genai
import json
import os
from rules import SEGURIDAD_SUPLEMENTOS

# ==========================================
# 1. CONFIGURACIÓN Y ESTILO VISUAL (CSS)
# ==========================================
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

def inyectar_estilo_quantum():
    st.markdown("""
        <style>
        /* Ocultar elementos nativos de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Ajuste fino de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #0E1117;
            border-right: 1px solid #262730;
        }
        
        /* Estilo elegante para Métricas (Contadores) */
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            color: #00FF94 !important; /* Verde Neón */
            font-weight: 700;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 14px !important;
            color: #a0a0a0 !important;
        }
        
        /* Botones Especiales */
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

inyectar_estilo_quantum() # Activamos el maquillaje

# ==========================================
# 2. SISTEMA DE PERSISTENCIA (LA MEMORIA)
# ==========================================
FILE_STATS = "quantum_stats.json"

def gestionar_estadisticas(tipo="leer"):
    # Si el archivo no existe, lo creamos en cero
    if not os.path.exists(FILE_STATS):
        with open(FILE_STATS, "w") as f:
            json.dump({"sesiones_totales": 0, "consultas_totales": 0}, f)
    
    with open(FILE_STATS, "r") as f:
        data = json.load(f)

    if tipo == "nueva_sesion":
        data["sesiones_totales"] += 1
    elif tipo == "nueva_consulta":
        data["consultas_totales"] += 1
    
    # Guardamos cambios si hubo escritura
    if tipo != "leer":
        with open(FILE_STATS, "w") as f:
            json.dump(data, f)
    
    return data

# ==========================================
# 3. CONEXIÓN NEURONAL (API KEY)
# ==========================================
try:
    # Buscamos la clave correcta GEMINI_API_KEY
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.error("⚠️ Error: No encuentro 'GEMINI_API_KEY' en secrets.toml")
        st.stop()
except Exception as e:
    st.error(f"Error de conexión: {e}")

# ==========================================
# 4. GESTIÓN DE SESIÓN
# ==========================================
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] 
if "alerta_fijada" not in st.session_state: st.session_state.alerta_fijada = None

# Detectar inicio de sesión única (para contar +1 vez al entrar)
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
# 6. BARRA LATERAL (CON DATOS HISTÓRICOS)
# ==========================================
stats_actuales = gestionar_estadisticas("leer") # Leemos los datos

with st.sidebar:
    st.success(f"👤 {st.session_state.usuario_activo}")
    
    # Métrica Doble
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Sesiones", stats_actuales["sesiones_totales"])
    col_m2.metric("Consultas", stats_actuales["consultas_totales"])
    
    st.markdown("---")
    st.subheader("🛠️ Panel de Control")
    nivel = st.radio("Nivel de IA:", ["Básica", "Media", "Experta"])
    
    with st.expander("📂 Recursos Administrativos"):
        st.caption("Accesos directos:")
        # Pega TUS LINKS REALES aquí abajo
        st.link_button("📝 Formulario de Alta", "https://forms.google.com/tu-link-real") 
        st.link_button("📊 Ver Hoja de Cálculo", "https://docs.google.com/spreadsheets/d/tu-link-real")
    
    st.markdown("---")
    if st.button("🗑️ Limpiar Chat"):
        st.session_state.messages = []
        st.session_state.alerta_fijada = None
        st.rerun()

# ==========================================
# 7. ZONA PRINCIPAL
# ==========================================
st.title("💊 Quantum Supplements")

# ALERTA PERSISTENTE
if st.session_state.alerta_fijada:
    val = st.session_state.alerta_fijada
    st.markdown(f"""
    <div style="border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px; background-color: rgba(255, 75, 75, 0.1); margin-bottom: 20px;">
        <h3 style="color: #FF4B4B; margin: 0;">🚨 RIESGO BIO-SISTÉMICO DETECTADO</h3>
        <p style="color: white; font-size: 1.1em;">Conflicto: <b>{val['sup'].upper()}</b> + <b>{val['condicion']}</b></p>
        <p style="color: white;">Se requiere validación médica antes de proceder.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.link_button(f"🩺 Ir a {val['esp']}", "https://quantum-health.streamlit.app", type="primary")

# PORTADA (Solo si está vacío y limpio)
if not st.session_state.messages and not st.session_state.alerta_fijada:
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=350)
    except: pass

# HISTORIAL DE CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 8. MOTOR DE INTELIGENCIA Y SEGURIDAD
# ==========================================
user_input = st.chat_input("Consulta sobre suplementos (ej: Zinc, Magnesio)...")

if user_input:
    # Guardamos mensaje y SUMAMOS +1 AL CONTADOR GLOBAL
    st.session_state.messages.append({"role": "user", "content": user_input})
    gestionar_estadisticas("nueva_consulta") # <--- Aquí actualizamos el histórico
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # REGLAS DE SEGURIDAD
    encontrado = False
    for sup, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup in user_input.lower():
            encontrado = True
            with st.chat_message("assistant", avatar="🧬"):
                st.warning(f"🛡️ **Protocolo de Seguridad: {sup.capitalize()}**")
                st.write(data["pregunta"])
                
                c1, c2 = st.columns(2)
                if c1.button("No, estoy sano"):
                    msg_ok = f"✅ Validación OK para {sup}. Procediendo al análisis..."
                    st.session_state.messages.append({"role": "assistant", "content": msg_ok})
                    st.rerun()
                
                if c2.button("Sí, tengo esa condición"):
                    st.session_state.alerta_fijada = {
                        "sup": sup,
                        "condicion": data["alerta_si"],
                        "esp": data["especialidad"]
                    }
                    st.rerun()
            break
            
    # RESPUESTA IA (Gemini)
    if not encontrado:
        with st.chat_message("assistant"):
            with st.spinner("🧠 Procesando bio-algoritmos..."):
                try:
                    prompt_sistema = f"""
                    Actúa como un Consultor Experto en Salud de Quantum Supplements.
                    Nivel de detalle: {nivel}.
                    Responde a: "{user_input}".
                    Usa formato estructurado con emojis (🧬, 💊, ⚠️).
                    """
                    
                    response = model.generate_content(prompt_sistema)
                    texto_respuesta = response.text
                    
                    st.markdown(texto_respuesta)
                    st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
                except Exception as e:
                    st.error(f"Error en el núcleo de IA: {e}")

    # Refrescamos para ver el contador nuevo
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