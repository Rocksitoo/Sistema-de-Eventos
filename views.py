import streamlit as st
from database import (create_user, get_all_records, get_generic_all_records, 
                     create_orders, get_user_events, delete_event)
from datetime import datetime

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
                with st.spinner("Registrando usuario..."):
                    try:
                        if create_user(nombre, password):
                            st.success("Usuario registrado exitosamente")
                            st.session_state.pagina = 'login'
                            st.rerun()
                        else:
                            st.error("Error al registrar usuario. El usuario podría ya existir.")
                    except Exception as e:
                        st.error(f"Error durante el registro: {str(e)}")

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
                try:
                    res = get_all_records(usuario, contrasena)
                    if res:
                        st.success("Inicio de sesión exitoso")
                        st.session_state.usuario = res[0]
                        st.session_state.pagina = 'eventos'
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos")
                except Exception as e:
                    st.error(f"Error durante el inicio de sesión: {str(e)}")

def mis_reservas():
    if 'usuario' not in st.session_state:
        st.warning("Por favor inicie sesión primero")
        st.session_state.pagina = 'login'
        st.rerun()
        return

    st.title("Mis Reservas")
    
    # Obtener las reservas del usuario
    reservas = get_user_events(st.session_state.usuario[0])
    
    if not reservas:
        st.info("No tienes reservas activas")
        if st.button("Hacer una nueva reserva"):
            st.session_state.pagina = 'eventos'
            st.rerun()
    else:
        # Mostrar las reservas en cards
        for reserva in reservas:
            id_evento, fecha, producto, cantidad, precio_total, descripcion = reserva
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(producto)
                    st.write(f"Fecha: {fecha.strftime('%d/%m/%Y')}")
                    st.write(f"Cantidad de personas: {cantidad}")
                    st.write(f"Precio total: ${precio_total:,.2f}")
                    with st.expander("Ver detalles"):
                        st.write(descripcion)
                
                with col2:
                    if st.button("Cancelar reserva", key=f"delete_{id_evento}"):
                        if delete_event(id_evento, st.session_state.usuario[0]):
                            st.success("Reserva cancelada exitosamente")
                            st.rerun()
                        else:
                            st.error("Error al cancelar la reserva")
                
                st.divider()
        
        if st.button("Hacer otra reserva"):
            st.session_state.pagina = 'eventos'
            st.rerun()

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
        fecha = st.date_input("Fecha del Evento", min_value=datetime.today())
        cantidad = st.number_input("Cantidad de personas", min_value=1, value=1)
        
        # Crear lista de opciones de productos
        opciones_productos = {f"{p[1]} - ${p[2]:,.2f}": p[0] for p in productos}
        producto_seleccionado = st.selectbox(
            "Seleccione el tipo de evento",
            options=list(opciones_productos.keys())
        )
        
        # Mostrar descripción del producto seleccionado
        id_producto = opciones_productos[producto_seleccionado]
        descripcion = next(p[3] for p in productos if p[0] == id_producto)
        st.info(descripcion)
        
        # Subir comprobante
        comprobante_file = st.file_uploader("Subir comprobante de pago", type=['pdf', 'png', 'jpg'])
        
        # Calcular precio total
        precio_unitario = next(p[2] for p in productos if p[0] == id_producto)
        precio_total = precio_unitario * cantidad
        
        st.write(f"Precio Total: ${precio_total:,.2f}")
        
        submitted = st.form_submit_button("Confirmar Reserva")
        
        if submitted:
            if not comprobante_file:
                st.error("Por favor suba el comprobante de pago")
            else:
                # Convertir el archivo a bytes para guardarlo en la base de datos
                comprobante_bytes = comprobante_file.getvalue()
                
                if create_orders(
                    fecha,
                    cantidad,
                    id_producto,
                    st.session_state.usuario[0],
                    comprobante_bytes,
                    precio_total
                ):
                    st.success("Reserva creada exitosamente")
                    # Redirigir a mis reservas
                    st.session_state.pagina = 'mis_reservas'
                    st.rerun()
                else:
                    st.error("Error al crear la reserva")
