-- Eliminar tablas si existen
DROP TABLE IF EXISTS eventos;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS usuarios;

-- Crear tabla usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(100) NOT NULL
);

-- Crear tabla productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT
);

-- Crear tabla eventos
CREATE TABLE eventos (
    id_evento SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    cantidad INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    comprobante BYTEA,
    precio_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Insertar productos de ejemplo
INSERT INTO productos (nombre, precio, descripcion) VALUES 
    ('Fiesta Básica', 1000.00, 'Paquete básico para 50 personas que incluye: Decoración básica, música, mesa de dulces');

INSERT INTO productos (nombre, precio, descripcion) VALUES 
    ('Fiesta Premium', 2000.00, 'Paquete premium para 100 personas que incluye: Decoración premium, DJ, buffet, mesa de dulces');

INSERT INTO productos (nombre, precio, descripcion) VALUES 
    ('Boda Elegante', 3000.00, 'Paquete especial para bodas que incluye: Decoración elegante, música en vivo, buffet, mesa de dulces');

INSERT INTO productos (nombre, precio, descripcion) VALUES 
    ('Fiesta Infantil', 800.00, 'Paquete especial para niños que incluye: Decoración temática, animador, juegos, pastel');
