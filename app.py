import streamlit as st
import datetime
from rules import SEGURIDAD_SUPLEMENTOS 

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

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
        if c.strip().upper() == "DEMO":
            st.session_state.usuario_activo = "Visitante Temporal"
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
    
    # --- AQUÍ ESTÁN TUS ENLACES RECUPERADOS ---
    with st.expander("📂 Recursos Administrativos"):
        st.caption("Accesos directos:")
        # Reemplaza estas URL con las tuyas reales de Google
        st.link_button("📝 Formulario de Alta", "https://forms.google.com/tu-formulario")
        st.link_button("📊 Ver Hoja de Cálculo", "https://docs.google.com/spreadsheets/d/tu-hoja")
    
    st.markdown("---")
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.session_state.alerta_fijada = None
        st.rerun()

# ==========================================
# 5. ZONA PRINCIPAL Y ALERTA DE ESPECIALISTA
# ==========================================
st.title("💊 Quantum Supplements")

# --- AQUÍ ESTÁ LA LÓGICA DE LA VENTANA DEL ESPECIALISTA ---
if st.session_state.alerta_fijada:
    val = st.session_state.alerta_fijada
    # Diseño de la alerta roja
    st.markdown(f"""
    <div style="border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px; background-color: rgba(255, 75, 75, 0.1); margin-bottom: 20px;">
        <h3 style="color: #FF4B4B; margin: 0;">🚨 RIESGO BIO-SISTÉMICO DETECTADO</h3>
        <p style="color: white; font-size: 1.1em;">Conflicto: <b>{val['sup'].upper()}</b> + <b>{val['condicion']}</b></p>
        <p style="color: white;">Se requiere validación médica antes de proceder.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ESTE ES EL BOTÓN QUE BUSCABAS (La "Ventana" de enlace)
    col_a, col_b = st.columns([1, 3])
    with col_a:
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
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 6.1 Revisión de Reglas de Seguridad (rules.py)
    encontrado = False
    for sup, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup in user_input.lower():
            encontrado = True
            with st.chat_message("assistant", avatar="🧬"):
                st.warning(f"🛡️ **Protocolo de Seguridad: {sup.capitalize()}**")
                st.write(data["pregunta"])
                
                # Botones de Acción
                c1, c2 = st.columns(2)
                if c1.button("No, estoy sano"):
                    st.session_state.messages.append({"role": "assistant", "content": f"✅ Validación OK para {sup}. Generando dosis..."})
                    st.rerun()
                
                if c2.button("Sí, tengo esa condición"):
                    # Activar la Alerta Persistente
                    st.session_state.alerta_fijada = {
                        "sup": sup,
                        "condicion": data["alerta_si"],
                        "esp": data["especialidad"]
                    }
                    st.rerun()
            break
            
    # 6.2 Respuesta IA (Si no hay reglas activas)
    if not encontrado:
        # Aquí iría tu conexión real a Gemini
        respuesta = f"Analizando '{user_input}' con IA (Nivel {nivel})..."
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
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