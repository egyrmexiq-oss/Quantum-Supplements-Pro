import streamlit as st
import google.generativeai as genai
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# ⚙️ CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Quantum Access Supplements", 
    page_icon="💊", 
    layout="wide"  # <--- AGREGA ESTA LÍNEA AQUÍ
)
# ==========================================
# 🔐 1. LOGIN DE SEGURIDAD
# ==========================================
st.set_page_config(page_title="Quantum Acsess Supplements", page_icon="💊")
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None

# ==========================================
# 🔐 1. LOGIN DE SEGURIDAD
# ==========================================
if "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None

if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum Supplements")
    
    # Animación 3D
    try: st.components.v1.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=400)
    except: pass
    
    # Música
    st.audio("https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3", loop=True, autoplay=True)
    
    # 👇 AQUÍ ESTÁ EL MENSAJE NUEVO
    st.info("🔑 Para ingresar, usa la clave: **DEMO**")
    
    c = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        # NOTA: Asegúrate de tener "DEMO" en tus 'secrets' o permite la entrada aquí
        # Modifiqué esto para que acepte "DEMO" directamente o busque en secrets
        if c.strip() == "DEMO" or (c.strip() in st.secrets["access_keys"]):
            # Si entra con DEMO, le ponemos un nombre genérico
            nombre = "Visitante" if c.strip() == "DEMO" else st.secrets["access_keys"][c.strip()]
            st.session_state.usuario_activo = nombre
            st.rerun()
        else: st.error("Acceso Denegado")
    st.stop()

# ==========================================
# 💎 2. CARGA DE DATOS
# ==========================================
try: genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except: st.error("Falta API Key")

URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTzh0kFdEwymIqv7sNd7dFpWCg09GtGipbYe0PMsKc_hzRbDoNLBHUk54ROdIceVGGZlYGeYM5HMgH0/pub?output=csv"
URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSdQBMZymJhY1mdEfKavnPpYnypaQ67S5Fp8AJ54L5n2P-Fvqg/viewform?usp=header"

@st.cache_data(ttl=60)
def cargar_medicos():
    try:
        df = pd.read_csv(URL_GOOGLE_SHEET)
        df.columns = [c.strip().lower() for c in df.columns]
        mapa = {}
        for col in df.columns:
            if "nombre" in col: mapa[col] = "nombre"
            elif "especialidad" in col: mapa[col] = "especialidad"
            elif "descripci" in col: mapa[col] = "descripcion"
            elif "tel" in col: mapa[col] = "telefono"
            elif "ciudad" in col: mapa[col] = "ciudad"
            elif "aprobado" in col: mapa[col] = "aprobado"
        df = df.rename(columns=mapa)
        if 'aprobado' in df.columns:
            return df[df['aprobado'].astype(str).str.upper().str.contains('SI')].to_dict(orient='records')
        return []
    except: return []

TODOS_LOS_MEDICOS = cargar_medicos()

# Preparación de la IA
if TODOS_LOS_MEDICOS:
    ciudades = sorted(list(set(str(m.get('ciudad', 'General')).title() for m in TODOS_LOS_MEDICOS)))
    ciudades.insert(0, "Todas las Ubicaciones")
    
    info_medicos = [f"ID: {m.get('nombre')} | Esp: {m.get('especialidad')} | Cd: {m.get('ciudad')}" for m in TODOS_LOS_MEDICOS]
    TEXTO_DIRECTORIO = "\n".join(info_medicos)
    
    INSTRUCCION_EXTRA = f"""
    ERES EL "MASTER COACH DE QUANTUM SUPPLEMENTS". Tu especialidad es la Nutrición Deportiva,
    el Fitness y la transformación física.

    1. IDENTIFICA EL OBJETIVO: Pregunta si el usuario busca: Aumentar Masa Muscular 💪, Perder Grasa 🔥, Energía/Pre-entreno ⚡ o Recuperación 🛌.
    2. RECOMENDACIONES PRECISAS: Sugiere productos específicos (Proteína Whey, Creatina, Quemadores, Vitaminas) basándote en su meta.
    3. SINERGIAS: Explica cómo combinar suplementos (ej. Creatina + Proteína).
    4. SEGURIDAD: Advierte siempre consultar a un médico antes de iniciar.
    5. EXPERTOS: Si necesitan una dieta o rutina personalizada, busca en esta lista: {TEXTO_DIRECTORIO} y recomienda al especialista ideal.
    """
else:
    ciudades = ["Mundo"]
    INSTRUCCION_EXTRA = "Actúa como médico general."

# ==========================================
# 📱 3. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    try: st.image("Logo_quantum.png", use_container_width=True)
    except: st.header("QUANTUM")
    
    st.success(f"Hola, {st.session_state.usuario_activo}")
    
    # --- CONTADOR DE VISITAS (Corregido) ---
    st.sidebar.divider() # Una linea divisoria bonita
    st.sidebar.write("📊 **Monitor de Tráfico**") # El título
    st.sidebar.markdown('<img src="https://api.visitorbadge.io/api/visitors?path=quantum-supplements-mx&countColor=%23ff5733&style=flat&label=Visitas" style="height: 25px;">',
    unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Ajustes")
    nivel = st.radio("Nivel de Respuesta:", ["Básica", "Media", "Experta"])
    
    if st.button("🗑️ Limpiar Chat"): st.session_state.mensajes = []; st.rerun()
    if st.button("🔒 Salir"): st.session_state.usuario_activo = None; st.rerun()

    st.markdown("---")
    st.markdown("### 👨‍⚕️ Directorio")
    if TODOS_LOS_MEDICOS:
        filtro = st.selectbox("📍 Ciudad:", ciudades)
        lista = TODOS_LOS_MEDICOS if filtro == "Todas las Ubicaciones" else [m for m in TODOS_LOS_MEDICOS if str(m.get('ciudad')).title() == filtro]
        
        if lista:
            if "idx" not in st.session_state: st.session_state.idx = 0
            m = lista[st.session_state.idx % len(lista)]
            
            # Tarjeta HTML
            tarjeta = (
                f'<div style="background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #444; margin-bottom: 10px;">'
                f'<h4 style="margin:0; color:white;">{m.get("nombre","Dr.")}</h4>'
                f'<div style="color:#00C2FF; font-weight:bold;">{m.get("especialidad")}</div>'
                f'<small style="color:#bbb;">{m.get("ciudad")}</small>'
                f'<div style="font-size: 0.9em; margin-top: 5px;">📞 {m.get("telefono","--")}</div>'
                f'</div>'
            )
            st.markdown(tarjeta, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            if c1.button("⬅️"): st.session_state.idx -= 1; st.rerun()
            if c2.button("➡️"): st.session_state.idx += 1; st.rerun()
        else: st.info("Sin resultados.")

    st.markdown("---")
    st.link_button("📝 Regístrate como Experto en Nutrición", URL_FORMULARIO)

# ==========================================
# 💬 4. CHAT PRINCIPAL
# ==========================================

st.markdown('<h1 style="text-align: center; color: #00C2FF;">Quantum AI Supplements</h1>', unsafe_allow_html=True)
st.caption(f"Asistente Médico Inteligente - Nivel {nivel}")

if "mensajes" not in st.session_state: 
    st.session_state.mensajes = [{"role": "assistant", "content": "Hola, soy Quantum. ¿Cómo te sientes hoy?"}]

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tus síntomas o dudas aquí..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    try:
        full_prompt = f"Eres Quantum (Nivel: {nivel}). {INSTRUCCION_EXTRA}. Usuario: {prompt}."
        # Usamos el modelo que TÚ tienes disponible según tu lista
        res = genai.GenerativeModel('gemini-2.5-flash').generate_content(full_prompt)
        st.session_state.mensajes.append({"role": "assistant", "content": res.text})
        st.rerun()
    except Exception as e: st.error(f"Error: {e}")
        # --- CÓDIGO TEMPORAL DE DIAGNÓSTICO ---
#if st.button("🕵️ Ver Modelos Disponibles"):
    #try:
        #st.write("Consultando a Google...")
        #for m in genai.list_models():
            #if 'generateContent' in m.supported_generation_methods:
                #st.code(f"Nombre: {m.name}")
    #except Exception as e:
        #st.error(f"Error: {e}")