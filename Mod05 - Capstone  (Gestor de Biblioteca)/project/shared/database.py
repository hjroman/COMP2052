from shared.config import DatabaseConfig

class DatabaseLayer:
    """Capa de datos compartida entre microservicios"""
    
    # ==================== USUARIOS ====================
    
    @staticmethod
    def get_user_by_username(username):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_all_users():
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username, nombre, rol FROM usuarios")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_user(username, password, nombre, rol):
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
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_user(user_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    # ==================== LIBROS ====================
    
    @staticmethod
    def get_all_books():
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libros")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_book_by_id(book_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM libros WHERE id = %s", (book_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_book(titulo, autor, isbn, año_publicacion, categoria):
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
            print(f"Error: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def update_book(book_id, titulo, autor, isbn, año_publicacion, categoria):
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
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_book(book_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM libros WHERE id = %s", (book_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def update_book_availability(book_id, disponible):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE libros SET disponible = %s WHERE id = %s", (disponible, book_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    # ==================== MIEMBROS ====================
    
    @staticmethod
    def get_all_members():
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM miembros")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_member_by_id(member_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM miembros WHERE id = %s", (member_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_member(nombre, apellido, correo, telefono):
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
            print(f"Error: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def update_member(member_id, nombre, apellido, correo, telefono):
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
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_member(member_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM miembros WHERE id = %s", (member_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    # ==================== PRÉSTAMOS ====================
    
    @staticmethod
    def get_all_loans():
        connection = DatabaseConfig.get_connection()
        if not connection:
            return []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM prestamos ORDER BY fecha_prestamo DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def get_loan_by_id(loan_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM prestamos WHERE id = %s", (loan_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def create_loan(libro_id, miembro_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return None
        try:
            cursor = connection.cursor()
            query = "INSERT INTO prestamos (libro_id, miembro_id, estado) VALUES (%s, %s, 'Activo')"
            cursor.execute(query, (libro_id, miembro_id))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def return_loan(loan_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            query = "UPDATE prestamos SET fecha_devolucion = NOW(), estado = 'Devuelto' WHERE id = %s"
            cursor.execute(query, (loan_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)
    
    @staticmethod
    def delete_loan(loan_id):
        connection = DatabaseConfig.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM prestamos WHERE id = %s", (loan_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            DatabaseConfig.close_connection(connection, cursor)