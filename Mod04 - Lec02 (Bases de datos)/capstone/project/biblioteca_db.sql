-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS biblioteca_db;

-- Usar la base de datos
USE biblioteca_db;

-- Tabla de Usuarios del Sistema (para login)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(500) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol ENUM('admin', 'bibliotecario') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Libros
CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    año_publicacion INT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Miembros (usuarios de la biblioteca)
CREATE TABLE IF NOT EXISTS miembros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Préstamos
CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro_id INT NOT NULL,
    miembro_id INT NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion TIMESTAMP NULL,
    estado ENUM('Activo', 'Devuelto') DEFAULT 'Activo',
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE,
    FOREIGN KEY (miembro_id) REFERENCES miembros(id) ON DELETE CASCADE
);

-- ⚠️ IMPORTANTE: No insertar usuarios aquí
-- Los usuarios se crearán ejecutando el script setup_users.py
-- Esto asegura que las contraseñas estén correctamente hasheadas

-- Insertar datos iniciales de libros
INSERT INTO libros (titulo, autor, isbn, año_publicacion, categoria, disponible) VALUES
('Cien Años de Soledad', 'Gabriel García Márquez', '978-0307474728', 1967, 'Ficción', TRUE),
('Don Quijote de la Mancha', 'Miguel de Cervantes', '978-8420412146', 1605, 'Clásico', TRUE),
('1984', 'George Orwell', '978-0451524935', 1949, 'Distopía', TRUE);

-- Insertar datos iniciales de miembros
INSERT INTO miembros (nombre, apellido, correo, telefono) VALUES
('María', 'González', 'maria.gonzalez@email.com', '787-123-4567'),
('Pedro', 'Martínez', 'pedro.martinez@email.com', '787-987-6543');