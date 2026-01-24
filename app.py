import streamlit as st
import google.generativeai as genai
from rules import SEGURIDAD_SUPLEMENTOS 

# ==========================================
# 1. CONFIGURACIÓN Y CONEXIÓN NEURONAL (CORREGIDO)
# ==========================================
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

# Intentamos conectar con la clave exacta que tienes en secrets.toml
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
    else:
        st.error("⚠️ Error Crítico: No encuentro 'GEMINI_API_KEY' en secrets.toml. Revisa el nombre.")
        st.stop() # Detenemos la app si no hay clave
except Exception as e:
    st.error(f"Error de conexión: {e}")

# ==========================================
# 2. GESTIÓN DE ESTADO (MEMORIA)
# ==========================================
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] 
if "alerta_fijada" not in st.session_state: st.session_state.alerta_fijada = None

# ==========================================
# 3. LOGIN DE SEGURIDAD
# ==========================================
if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum Supplements")
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=400)
    except: pass
    
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        # Verificamos si la clave es DEMO o alguna de las configuradas
        claves = st.secrets.get("access_keys", {})
        if c.strip().upper() == "DEMO":
            st.session_state.usuario_activo = "Visitante Temporal"
            st.rerun()
        elif c in claves:
            st.session_state.usuario_activo = claves[c]
            st.rerun()
    st.stop()

# ==========================================
# 4. BARRA LATERAL (ADMIN Y RECURSOS)
# ==========================================
with st.sidebar:
    st.success(f"👤 {st.session_state.usuario_activo}")
    st.metric("Mensajes en sesión", len(st.session_state.messages))
    
    st.markdown("---")
    st.subheader("🛠️ Panel de Control")
    nivel = st.radio("Nivel de IA:", ["Básica", "Media", "Experta"])
    
    with st.expander("📂 Recursos Administrativos"):
        st.caption("Accesos directos:")
        st.link_button("📝 Formulario de Alta", "https://forms.google.com/tu-formulario-real") # <--- Pega tu link aquí
        st.link_button("📊 Ver Hoja de Cálculo", "https://docs.google.com/spreadsheets/d/tu-hoja-real") # <--- Pega tu link aquí
    
    st.markdown("---")
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.session_state.alerta_fijada = None
        st.rerun()

# ==========================================
# 5. ZONA PRINCIPAL Y ALERTA DE ESPECIALISTA
# ==========================================
st.title("💊 Quantum Supplements")

# LÓGICA DE LA VENTANA ROJA (PERSISTENTE)
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
        # AQUÍ ESTÁ EL BOTÓN DE ESPECIALISTAS
        st.link_button(f"🩺 Ir a {val['esp']}", "https://quantum-health.streamlit.app", type="primary")

# Portada (Solo si no hay mensajes y no hay alerta)
if not st.session_state.messages and not st.session_state.alerta_fijada:
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=350)
    except: pass

# Renderizar Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 6. MOTOR DE INTELIGENCIA Y SEGURIDAD
# ==========================================
user_input = st.chat_input("Consulta sobre suplementos (ej: Zinc, Magnesio)...")

if user_input:
    # 1. Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 2. Revisión de Reglas de Seguridad (rules.py)
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
            
    # 3. Respuesta IA REAL (Google Gemini)
    if not encontrado:
        with st.chat_message("assistant"):
            with st.spinner("🧠 Procesando bio-algoritmos..."):
                try:
                    # Prompt de Ingeniería para Gemini
                    prompt_sistema = f"""
                    Actúa como un Consultor Experto en Salud de Quantum Supplements.
                    El usuario tiene un nivel de conocimiento: {nivel}.
                    Responde a la consulta: "{user_input}".
                    
                    Estructura tu respuesta así:
                    1. 🧬 **Beneficio Principal**
                    2. 💊 **Dosis Sugerida** (General)
                    3. ⚠️ **Precaución Breve**
                    
                    Mantén un tono profesional, empático y futurista.
                    """
                    
                    # LLAMADA REAL A LA API
                    response = model.generate_content(prompt_sistema)
                    texto_respuesta = response.text
                    
                    st.markdown(texto_respuesta)
                    st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
                except Exception as e:
                    st.error(f"Error en el núcleo de IA: {e}")
        # --- CÓDIGO TEMPORAL DE DIAGNÓSTICO ---
#if st.button("🕵️ Ver Modelos Disponibles"):
    #try:
        #st.write("Consultando a Google...")
        #for m in genai.list_models():
            #if 'generateContent' in m.supported_generation_methods:
                #st.code(f"Nombre: {m.name}")
    #except Exception as e:
        #st.error(f"Error: {e}")