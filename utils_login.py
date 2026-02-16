import streamlit as st
import time

def validar_acceso():
    """
    Maneja el login con seguridad anti-fuerza bruta.
    Retorna: El rol del usuario (str) si es exitoso, o None si no.
    """
    
    # 1. Inicializar variables de seguridad en la sesión
    if "intentos_fallidos" not in st.session_state:
        st.session_state.intentos_fallidos = 0
    if "login_bloqueado" not in st.session_state:
        st.session_state.login_bloqueado = False

    # 2. Verificar si ya está bloqueado
    if st.session_state.login_bloqueado:
        st.error("⛔ ACCESO BLOQUEADO: Demasiados intentos fallidos.")
        st.caption("Por seguridad, debes recargar la página para intentar de nuevo.")
        st.stop() # Detiene la ejecución de la app aquí

    # 3. Verificar si ya hay usuario logueado
    if "usuario_activo" in st.session_state and st.session_state.usuario_activo:
        return st.session_state.usuario_activo

    # 4. Interfaz de Login
    st.markdown("## 🔐 Acceso Seguro")
    
    # Animación pequeña (Opcional, la misma que tenías)
    try:
        import streamlit.components.v1 as components
        # Usamos un iframe más pequeño o solo texto para cargar rápido
        pass 
    except: pass

    with st.form("form_login"):
        clave_input = st.text_input("Ingresa tu Clave de Acceso:", type="password")
        submit = st.form_submit_button("Ingresar")

        if submit:
            # A) Retraso artificial para frustrar bots (1 segundo)
            time.sleep(1) 
            
            # B) Limpieza de input
            clave_limpia = clave_input.strip() # Respetamos mayúsculas/minúsculas de tu TOML original o forzamos? 
            # Si en tu TOML las claves están exactas, mejor no hacer .upper() para dar más entropía.
            
            # C) Buscar en Secrets
            # Asumimos que en secrets.toml tienes una sección [access_keys]
            claves_validas = st.secrets.get("access_keys", {})
            
            if clave_limpia in claves_validas:
                # --- ÉXITO ---
                rol = claves_validas[clave_limpia]
                st.session_state.usuario_activo = rol
                st.session_state.intentos_fallidos = 0 # Resetear contador
                st.success(f"Bienvenido: {rol}")
                time.sleep(0.5)
                st.rerun()
            else:
                # --- FALLO ---
                st.session_state.intentos_fallidos += 1
                intentos_restantes = 3 - st.session_state.intentos_fallidos
                
                if intentos_restantes <= 0:
                    st.session_state.login_bloqueado = True
                    st.error("⛔ Has excedido el número de intentos.")
                    st.rerun()
                else:
                    st.warning(f"Clave incorrecta. Intentos restantes: {intentos_restantes}")
                    # Castigo extra de tiempo si fallan seguido
                    time.sleep(st.session_state.intentos_fallidos) 
                    
    return None
