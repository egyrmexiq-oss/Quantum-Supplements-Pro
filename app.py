import streamlit as st
import google.generativeai as genai
import json
import os
from rules import SEGURIDAD_SUPLEMENTOS

# ==========================================
# 1. CONFIGURACIÓN Y ESTILO VISUAL
# ==========================================
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

def inyectar_estilo_quantum():
    st.markdown("""
        <style>
        /* Ocultar elementos nativos */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Sidebar oscura y elegante */
        [data-testid="stSidebar"] {
            background-color: #0E1117;
            border-right: 1px solid #262730;
        }
        
        /* Métricas (Contadores) en Verde Neón */
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            color: #00FF94 !important;
            font-weight: 700;
        }
        
        /* Botones Primarios */
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
# 2. SISTEMA DE PERSISTENCIA (ESTADÍSTICAS)
# ==========================================
FILE_STATS = "quantum_stats.json"

def gestionar_estadisticas(tipo="leer"):
    # Crear archivo si no existe
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
# 3. CONEXIÓN NEURONAL
# ==========================================
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # ⚠️ AQUÍ PUEDES CAMBIAR EL NOMBRE DEL MODELO SI PREFIERES OTRO
        # Opciones: 'gemini-1.5-flash', 'gemini-2.0-flash-exp'
        model = genai.GenerativeModel('gemini-2.5-flash')
    else:
        st.error("⚠️ Error: No encuentro 'GEMINI_API_KEY' en secrets.toml")
        st.stop()
except Exception as e:
    st.error(f"Error de conexión: {e}")

# ==========================================
# 4. GESTIÓN DE MEMORIA (ANTI-BUCLE)
# ==========================================
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] 
if "alerta_fijada" not in st.session_state: st.session_state.alerta_fijada = None

# ¡ESTA ES LA SOLUCIÓN AL CICLADO!
# Creamos un conjunto para recordar qué suplementos ya fueron validados como seguros
if "validaciones_ok" not in st.session_state: st.session_state.validaciones_ok = set()

# Contador de sesiones únicas
if "sesion_iniciada" not in st.session_state:
    gestionar_estadisticas("nueva_sesion")
    st.session_state.sesion_iniciada = True

# ==========================================
# 5. LOGIN DE SEGURIDAD
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
# 6. BARRA LATERAL (PANEL DE CONTROL)
# ==========================================
stats_actuales = gestionar_estadisticas("leer")

with st.sidebar:
    st.success(f"👤 {st.session_state.usuario_activo}")
    
    col1, col2 = st.columns(2)
    col1.metric("Sesiones", stats_actuales["sesiones_totales"])
    col2.metric("Consultas", stats_actuales["consultas_totales"])
    
    st.markdown("---")
    st.subheader("🛠️ Configuración IA")
    nivel = st.radio("Nivel de Detalle:", ["Básica", "Media", "Experta"])
    
    with st.expander("📂 Recursos Administrativos"):
        st.caption("Enlaces Rápidos:")
        # Pega tus enlaces reales aquí
        st.link_button("📝 Formulario de Alta", "https://forms.google.com/...") 
        st.link_button("📊 Hoja de Cálculo", "https://docs.google.com/spreadsheets/...")
    
    st.markdown("---")
    if st.button("🗑️ Reiniciar Chat"):
        st.session_state.messages = []
        st.session_state.alerta_fijada = None
        st.session_state.validaciones_ok = set() # Borramos la memoria de validaciones
        st.rerun()

# ==========================================
# 7. ZONA PRINCIPAL
# ==========================================
st.title("💊 Quantum Supplements")

# SI HAY ALERTA ROJA (PERSISTENTE)
if st.session_state.alerta_fijada:
    val = st.session_state.alerta_fijada
    st.markdown(f"""
    <div style="border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px; background-color: rgba(255, 75, 75, 0.1); margin-bottom: 20px;">
        <h3 style="color: #FF4B4B; margin: 0;">🚨 RIESGO DETECTADO</h3>
        <p style="color: white;">Conflicto Crítico: <b>{val['sup'].upper()}</b> + <b>{val['condicion']}</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button(f"🩺 Contactar a {val['esp']}", "https://quantum-health.streamlit.app", type="primary")

# PORTADA (Solo si chat vacío y sin alertas)
if not st.session_state.messages and not st.session_state.alerta_fijada:
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=350)
    except: pass

# MOSTRAR HISTORIAL
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 8. CEREBRO Y SEGURIDAD (ANTI-BUCLE)
# ==========================================
user_input = st.chat_input("Escribe tu consulta sobre suplementos...")

if user_input:
    # 1. Guardar input y sumar estadística
    st.session_state.messages.append({"role": "user", "content": user_input})
    gestionar_estadisticas("nueva_consulta")
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 2. VALIDACIÓN DE SEGURIDAD
    bloqueo_seguridad = False
    
    for sup, data in SEGURIDAD_SUPLEMENTOS.items():
        # LÓGICA CLAVE: Si encuentra el suplemento Y NO está en la lista de "Aprobados"
        if sup in user_input.lower() and sup not in st.session_state.validaciones_ok:
            bloqueo_seguridad = True
            
            with st.chat_message("assistant", avatar="🛡️"):
                st.warning(f"**Protocolo de Seguridad: {sup.capitalize()}**")
                st.write(data["pregunta"])
                
                c1, c2 = st.columns(2)
                
                # OPCIÓN A: NO TENGO RIESGO
                if c1.button("No, estoy sano"):
                    # Agregamos a la lista blanca para que NO vuelva a preguntar
                    st.session_state.validaciones_ok.add(sup)
                    
                    # Mensaje de confirmación
                    st.session_state.messages.append({"role": "assistant", "content": f"✅ Validación completada para **{sup}**. Procesando..."})
                    st.rerun() # Recargamos para que el código fluya limpio
                
                # OPCIÓN B: SÍ TENGO RIESGO
                if c2.button("Sí, tengo esa condición"):
                    st.session_state.alerta_fijada = {
                        "sup": sup,
                        "condicion": data["alerta_si"],
                        "esp": data["especialidad"]
                    }
                    st.rerun()
            break # Paramos el loop para esperar respuesta
    
    # 3. RESPUESTA IA (Solo si no hay bloqueo de seguridad activo)
    if not bloqueo_seguridad:
        with st.chat_message("assistant"):
            with st.spinner("🧠 Analizando con IA..."):
                try:
                    prompt = f"""
                    Actúa como Experto en Suplementos de Quantum Health.
                    Nivel: {nivel}.
                    Usuario pregunta: "{user_input}".
                    Responde con estructura clara: Beneficio 🧬, Dosis 💊, Precaución ⚠️.
                    """
                    
                    response = model.generate_content(prompt)
                    res_text = response.text
                    
                    st.markdown(res_text)
                    st.session_state.messages.append({"role": "assistant", "content": res_text})
                
                except Exception as e:
                    # Captura de error visible
                    err_msg = f"⚠️ **Error de IA:** {str(e)}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
    # Recargamos para ver el resultado
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