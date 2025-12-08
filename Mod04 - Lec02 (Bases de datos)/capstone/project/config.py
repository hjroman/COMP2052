import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    """Configuración de la base de datos MySQL"""
    
    HOST = "localhost"
    USER = "root"
    PASSWORD = ""  # Cambiar por tu contraseña de MySQL
    DATABASE = "biblioteca_db"
    PORT = 3306
    
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos"""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE,
                port=DatabaseConfig.PORT
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None
    
    @staticmethod
    def close_connection(connection, cursor=None):
        """Cierra la conexión y el cursor si existen"""
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()