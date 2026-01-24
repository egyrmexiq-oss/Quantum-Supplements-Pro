import streamlit as st
import google.generativeai as genai
from rules import SEGURIDAD_SUPLEMENTOS 

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Quantum Access Supplements", page_icon="💊", layout="wide")

# 2. INICIALIZACIÓN DE ESTADOS (MEMORIA)
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None
if "messages" not in st.session_state: st.session_state.messages = [] 
if "alerta_activa" not in st.session_state: st.session_state.alerta_activa = None

# 3. LOGIN
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

# 4. BARRA LATERAL (SIDEBAR LIMPIA)
with st.sidebar:
    st.success(f"👤 {st.session_state.usuario_activo}")
    # Solo un contador, usando la métrica oficial de Streamlit
    st.metric("Mensajes en sesión", len(st.session_state.messages))
    
    st.markdown("---")
    nivel = st.radio("Nivel de Respuesta:", ["Básica", "Media", "Experta"])
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.messages = []
        st.session_state.alerta_activa = None
        st.rerun()
    if st.button("🔒 Salir"):
        st.session_state.clear()
        st.rerun()

# 5. CUERPO PRINCIPAL Y PORTADA
st.title("💊 Quantum Supplements")

# Si hay una alerta de riesgo guardada, la mostramos siempre arriba
if st.session_state.alerta_activa:
    data = st.session_state.alerta_activa
    st.error(f"🚨 **RIESGO DETECTADO:** {data['sup'].upper()}")
    st.markdown(f"Debido a: *{data['condicion']}*, es necesaria una validación profesional.")
    st.link_button(f"🔎 Contactar Especialista en {data['esp']}", "https://quantum-health.streamlit.app")
    st.markdown("---")

# Portada solo si no hay charla
if not st.session_state.messages:
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=300)
    except: pass
    st.info("Escribe el nombre de un suplemento (ej: Magnesio) para iniciar el protocolo.")

# Render historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. LÓGICA DE INTERACCIÓN
user_input = st.chat_input("Escribe tu consulta...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Revisar seguridad
    for sup_key, data in SEGURIDAD_SUPLEMENTOS.items():
        if sup_key in user_input.lower():
            with st.chat_message("assistant", avatar="🧬"):
                st.warning(f"🛡️ **Protocolo Quantum: {sup_key.capitalize()}**")
                st.write(data["pregunta"])
                
                # Usamos columnas para los botones de respuesta rápida
                col_no, col_si = st.columns(2)
                if col_no.button("No tengo riesgos"):
                    st.session_state.messages.append({"role": "assistant", "content": f"✅ Validación superada para {sup_key}."})
                    st.rerun()
                if col_si.button("Sí, tengo esa condición"):
                    # GUARDAMOS LA ALERTA EN LA MEMORIA DE SESIÓN
                    st.session_state.alerta_activa = {
                        "sup": sup_key,
                        "condicion": data['alerta_si'],
                        "esp": data['especialidad']
                    }
                    st.rerun()
            break
    else:
        # Respuesta normal de IA si no hay keyword de seguridad
        respuesta = f"Analizando {user_input}..." 
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.rerun()
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