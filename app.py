import streamlit as st
from views import registro, iniciar_sesion, eventos

# Inicializar el estado de la sesión si no existe
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'

# Crear el sidebar
with st.sidebar:
    st.title("Menú")
    opciones = {
        'Iniciar Sesión': 'login',
        'Registrarse': 'registro',
        'Eventos': 'eventos'
    }
    
    for opcion, valor in opciones.items():
        if st.button(opcion):
            st.session_state.pagina = valor
            st.rerun()
    
    # Botón de cerrar sesión
    if 'usuario' in st.session_state:
        if st.button("Cerrar Sesión"):
            del st.session_state.usuario
            st.session_state.pagina = 'login'
            st.rerun()

# Mostrar la página correspondiente
if st.session_state.pagina == 'login':
    iniciar_sesion()
elif st.session_state.pagina == 'registro':
    registro()
elif st.session_state.pagina == 'eventos':
    eventos()