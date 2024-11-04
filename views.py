import streamlit as st
from database import get_all_records, create_user, get_generic_all_records, create_orders
from datetime import datetime
import io

def registro():
    st.title("Registro de Usuario")
    
    with st.form("registro_form"):
        nombre = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        confirm_password = st.text_input("Confirmar Contraseña", type="password")
        
        submitted = st.form_submit_button("Registrarse")
        
        if submitted:
            if not nombre or not password or not confirm_password:
                st.error("Por favor complete todos los campos")
            elif password != confirm_password:
                st.error("Las contraseñas no coinciden")
            else:
                if create_user(nombre, password):
                    st.success("Usuario registrado exitosamente")
                    st.session_state.pagina = 'login'
                    st.rerun()
                else:
                    st.error("Error al registrar usuario")

def iniciar_sesion():
    st.title("Iniciar Sesión")
    
    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar")
        
        if submitted:
            if not usuario or not contrasena:
                st.error("Por favor complete todos los campos")
            else:
                res = get_all_records(usuario, contrasena)
                if res:
                    st.success("Inicio de sesión exitoso")
                    st.session_state.usuario = res[0]
                    st.session_state.pagina = 'eventos'
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")

def eventos():
    if 'usuario' not in st.session_state:
        st.warning("Por favor inicie sesión primero")
        st.session_state.pagina = 'login'
        st.rerun()
        return

    st.title("Reserva de Eventos")
    
    # Obtener lista de productos/servicios disponibles
    productos = get_generic_all_records('productos')
    
    with st.form("evento_form"):
        fecha = st.date_input("Fecha del Evento")
        cantidad = st.number_input("Cantidad de personas", min_value=1, value=1)
        
        # Crear lista de opciones de productos
        opciones_productos = {f"{p[1]} - ${p[2]}": p[0] for p in productos}
        producto_seleccionado = st.selectbox(
            "Seleccione el tipo de evento",
            options=list(opciones_productos.keys())
        )
        
        # Subir comprobante
        comprobante_file = st.file_uploader("Subir comprobante de pago", type=['pdf', 'png', 'jpg'])
        
        # Calcular precio total
        id_producto = opciones_productos[producto_seleccionado]
        precio_unitario = next(p[2] for p in productos if p[0] == id_producto)
        precio_total = precio_unitario * cantidad
        
        st.write(f"Precio Total: ${precio_total}")
        
        submitted = st.form_submit_button("Confirmar Reserva")
        
        if submitted:
            if not comprobante_file:
                st.error("Por favor suba el comprobante de pago")
            else:
                # Convertir el archivo a bytes para guardarlo en la base de datos
                comprobante_bytes = io.BytesIO(comprobante_file.getvalue()).read()
                
                if create_orders(
                    fecha,
                    cantidad,
                    id_producto,
                    st.session_state.usuario[0],
                    comprobante_bytes,
                    precio_total
                ):
                    st.success("Reserva creada exitosamente")
                else:
                    st.error("Error al crear la reserva")