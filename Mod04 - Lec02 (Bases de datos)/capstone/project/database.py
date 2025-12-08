from config import DatabaseConfig
from datetime import datetime

class DatabaseLayer:
    """Capa de datos para manejar todas las operaciones de base de datos"""
    
    # ==================== USUARIOS DEL SISTEMA ====================
    
    @staticmethod
    def get_user_by_username(username):
        """Obtiene un usuario por su username"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios del sistema"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username, nombre, rol FROM usuarios")
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_user(username, password, nombre, rol):
        """Crea un nuevo usuario del sistema"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "INSERT INTO usuarios (username, password, nombre, rol) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, password, nombre, rol))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario del sistema"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    # ==================== LIBROS ====================
    
    @staticmethod
    def get_all_books():
        """Obtiene todos los libros"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libros")
            books = cursor.fetchall()
            return books
        except Exception as e:
            print(f"Error al obtener libros: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_book_by_id(book_id):
        """Obtiene un libro por su ID"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libros WHERE id = %s", (book_id,))
            book = cursor.fetchone()
            return book
        except Exception as e:
            print(f"Error al obtener libro: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_book(titulo, autor, isbn, año_publicacion, categoria):
        """Crea un nuevo libro"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            query = """INSERT INTO libros (titulo, autor, isbn, año_publicacion, categoria, disponible) 
                       VALUES (%s, %s, %s, %s, %s, TRUE)"""
            cursor.execute(query, (titulo, autor, isbn, año_publicacion, categoria))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear libro: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def update_book(book_id, titulo, autor, isbn, año_publicacion, categoria):
        """Actualiza un libro"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = """UPDATE libros SET titulo = %s, autor = %s, isbn = %s, 
                       año_publicacion = %s, categoria = %s WHERE id = %s"""
            cursor.execute(query, (titulo, autor, isbn, año_publicacion, categoria, book_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar libro: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_book(book_id):
        """Elimina un libro"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM libros WHERE id = %s", (book_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def update_book_availability(book_id, disponible):
        """Actualiza la disponibilidad de un libro"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE libros SET disponible = %s WHERE id = %s", (disponible, book_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar disponibilidad: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    # ==================== MIEMBROS ====================
    
    @staticmethod
    def get_all_members():
        """Obtiene todos los miembros"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM miembros")
            members = cursor.fetchall()
            return members
        except Exception as e:
            print(f"Error al obtener miembros: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_member_by_id(member_id):
        """Obtiene un miembro por su ID"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM miembros WHERE id = %s", (member_id,))
            member = cursor.fetchone()
            return member
        except Exception as e:
            print(f"Error al obtener miembro: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_member(nombre, apellido, correo, telefono):
        """Crea un nuevo miembro"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            query = "INSERT INTO miembros (nombre, apellido, correo, telefono) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, apellido, correo, telefono))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear miembro: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def update_member(member_id, nombre, apellido, correo, telefono):
        """Actualiza un miembro"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "UPDATE miembros SET nombre = %s, apellido = %s, correo = %s, telefono = %s WHERE id = %s"
            cursor.execute(query, (nombre, apellido, correo, telefono, member_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar miembro: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_member(member_id):
        """Elimina un miembro"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM miembros WHERE id = %s", (member_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar miembro: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    # ==================== PRÉSTAMOS ====================
    
    @staticmethod
    def get_all_loans():
        """Obtiene todos los préstamos"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM prestamos ORDER BY fecha_prestamo DESC")
            loans = cursor.fetchall()
            return loans
        except Exception as e:
            print(f"Error al obtener préstamos: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_loan_by_id(loan_id):
        """Obtiene un préstamo por su ID"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM prestamos WHERE id = %s", (loan_id,))
            loan = cursor.fetchone()
            return loan
        except Exception as e:
            print(f"Error al obtener préstamo: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_loan(libro_id, miembro_id):
        """Crea un nuevo préstamo"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            query = "INSERT INTO prestamos (libro_id, miembro_id, estado) VALUES (%s, %s, 'Activo')"
            cursor.execute(query, (libro_id, miembro_id))
            connection.commit()
            
            # Actualizar disponibilidad del libro
            DatabaseLayer.update_book_availability(libro_id, False)
            
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear préstamo: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def return_loan(loan_id):
        """Marca un préstamo como devuelto"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            # Obtener el préstamo para saber qué libro liberar
            loan = DatabaseLayer.get_loan_by_id(loan_id)
            if not loan:
                return False
            
            cursor = connection.cursor()
            query = "UPDATE prestamos SET fecha_devolucion = NOW(), estado = 'Devuelto' WHERE id = %s"
            cursor.execute(query, (loan_id,))
            connection.commit()
            
            # Actualizar disponibilidad del libro
            DatabaseLayer.update_book_availability(loan['libro_id'], True)
            
            return True
        except Exception as e:
            print(f"Error al devolver préstamo: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_loan(loan_id):
        """Elimina un préstamo"""
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM prestamos WHERE id = %s", (loan_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar préstamo: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)