"""
Script para crear usuarios iniciales con contraseñas hasheadas correctamente
Ejecutar este script después de crear la base de datos
"""

from werkzeug.security import generate_password_hash
from config import DatabaseConfig

def create_initial_users():
    """Crea los usuarios iniciales en la base de datos"""
    
    # Generar hashes de contraseñas
    admin_password = generate_password_hash("admin123")
    biblio_password = generate_password_hash("biblio123")
    
    print("Generando contraseñas hasheadas...")
    print(f"Admin hash: {admin_password[:50]}...")
    print(f"Bibliotecario hash: {biblio_password[:50]}...")
    
    # Conectar a la base de datos
    connection = DatabaseConfig.get_connection()
    
    if not connection:
        print("❌ Error: No se pudo conectar a la base de datos")
        print("Verifica que MySQL esté corriendo y que config.py tenga los datos correctos")
        return
    
    try:
        cursor = connection.cursor()
        
        # Limpiar tabla de usuarios si existe
        print("\nLimpiando usuarios existentes...")
        cursor.execute("DELETE FROM usuarios")
        connection.commit()
        
        # Insertar usuarios con contraseñas hasheadas
        print("Insertando nuevos usuarios...")
        
        query = "INSERT INTO usuarios (username, password, nombre, rol) VALUES (%s, %s, %s, %s)"
        
        # Usuario Admin
        cursor.execute(query, ('admin', admin_password, 'Administrador', 'admin'))
        print("✅ Usuario 'admin' creado")
        
        # Usuario Bibliotecario
        cursor.execute(query, ('bibliotecario', biblio_password, 'Juan Bibliotecario', 'bibliotecario'))
        print("✅ Usuario 'bibliotecario' creado")
        
        connection.commit()
        
        print("\n" + "="*50)
        print("✅ USUARIOS CREADOS EXITOSAMENTE")
        print("="*50)
        print("\nCredenciales de acceso:")
        print("  👨‍💼 Admin:")
        print("     Usuario: admin")
        print("     Contraseña: admin123")
        print("\n  👤 Bibliotecario:")
        print("     Usuario: bibliotecario")
        print("     Contraseña: biblio123")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error al crear usuarios: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
        print("\nConexión cerrada.")

if __name__ == "__main__":
    print("="*50)
    print("SCRIPT DE CREACIÓN DE USUARIOS INICIALES")
    print("="*50)
    create_initial_users()