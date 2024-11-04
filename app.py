import streamlit as st
from views import registro, iniciar_sesion, eventos, mis_reservas

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Eventos",
    page_icon="🎉",
    layout="wide"
)

# Inicializar el estado de la sesión si no existe
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'

# Crear el sidebar
with st.sidebar:
    st.title("Menú")
    
    if 'usuario' not in st.session_state:
        # Menú para usuarios no autenticados
        opciones = {
            'Iniciar Sesión': 'login',
            'Registrarse': 'registro'
        }
    else:
        # Menú para usuarios autenticados
        st.write(f"Bienvenido, {st.session_state.usuario[1]}")
        opciones = {
            'Reservar Evento': 'eventos',
            'Mis Reservas': 'mis_reservas'
        }
    
    for opcion, valor in opciones.items():
        if st.button(opcion):
            st.session_state.pagina = valor
            st.rerun()
    
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
elif st.session_state.pagina == 'mis_reservas':
    mis_reservas()
