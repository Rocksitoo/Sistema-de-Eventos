import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="eventos_vkue",
            user="eventos_vkue_user",
            password="pa7v3fUvzDVMhMOI5f5vqGrptezz9KGd",
            host="dpg-cskhh63tq21c73dot5b0-a.oregon-postgres.render.com",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error de conexión: {str(e)}")
        return None

def create_user(nombre, contraseña):
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            print("No se pudo establecer la conexión")
            return False
            
        cur = conn.cursor()
        # Verificar si el usuario ya existe
        cur.execute("SELECT nombre FROM usuarios WHERE nombre = %s", (nombre,))
        if cur.fetchone() is not None:
            print("El usuario ya existe")
            return False
            
        sql = "INSERT INTO usuarios (nombre, contraseña) VALUES (%s, %s)"
        cur.execute(sql, (nombre, contraseña))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al crear usuario: {str(e)}")
        return False
    finally:
        if conn:
            if 'cur' in locals():
                cur.close()
            conn.close()

def get_all_records(nombre, contrasena):
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return None
            
        cur = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s"
        cur.execute(sql, (nombre, contrasena))
        records = cur.fetchall()
        return records
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        if conn:
            if 'cur' in locals():
                cur.close()
            conn.close()

def get_generic_all_records(tabla):
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return None
            
        cur = conn.cursor()
        sql = f"SELECT * FROM {tabla}"
        cur.execute(sql)
        records = cur.fetchall()
        return records
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        if conn:
            if 'cur' in locals():
                cur.close()
            conn.close()

def create_orders(fecha, cantidad, id_producto, id_usuario, comprobante, precio_total):
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return False
            
        cur = conn.cursor()
        sql = """
        INSERT INTO eventos (fecha, cantidad, id_producto, id_usuario, comprobante, precio_total) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (fecha, cantidad, id_producto, id_usuario, comprobante, precio_total))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        if conn:
            if 'cur' in locals():
                cur.close()
            conn.close()

def get_user_events(id_usuario):
    """Obtiene todas las reservas de un usuario específico"""
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return None
            
        cur = conn.cursor()
        sql = """
        SELECT 
            e.id_evento,
            e.fecha,
            p.nombre as producto,
            e.cantidad,
            e.precio_total,
            p.descripcion
        FROM eventos e
        JOIN productos p ON e.id_producto = p.id_producto
        WHERE e.id_usuario = %s
        ORDER BY e.fecha DESC
        """
        cur.execute(sql, (id_usuario,))
        records = cur.fetchall()
        return records
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        if conn:
            if 'cur' in locals():
                cur.close()
            conn.close()

def delete_event(id_evento, id_usuario):
    """Elimina una reserva específica de un usuario"""
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return False
            
        cur = conn.cursor()
        # Verificar que el evento pertenece al usuario
        sql = "DELETE FROM eventos WHERE id_evento = %s AND id_usuario = %s"
        cur.execute(sql, (id_evento, id_usuario))
        rows_deleted = cur.rowcount
        conn.commit()
        return rows_deleted > 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        if conn:
            if 'cur' in locals():
                cur.close()
            conn.close()
