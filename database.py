import psycopg2
from psycopg2 import Error

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="neondb",
            user="neondb_owner",
            password="UM8qYDASVB0s",
            host="ep-soft-morning-a57gvomn.us-east-2.aws.neon.tech",
            port="5432",
            sslmode='require'
        )
        return conn
    except Error as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return None

def get_all_records(nombre, contrasena):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s"
        cur.execute(sql, (nombre, contrasena))
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except Error as e:
        print(f"Error: {e}")
        return None

def create_user(nombre, contraseña):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = "INSERT INTO usuarios (nombre, contraseña) VALUES (%s, %s)"
        cur.execute(sql, (nombre, contraseña))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False

def get_generic_all_records(tabla):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = f"SELECT * FROM {tabla}"
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except Error as e:
        print(f"Error: {e}")
        return None

def create_orders(fecha, cantidad, id_producto, id_usuario, comprobante, precio_total):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        INSERT INTO eventos (fecha, cantidad, id_producto, id_usuario, comprobante, precio_total) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (fecha, cantidad, id_producto, id_usuario, comprobante, precio_total))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False