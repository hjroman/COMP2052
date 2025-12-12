# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Base de datos SQLite en un archivo llamado inventory.db
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "inventory.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta para manejar sesiones y mensajes flash
    SECRET_KEY = "cambia_esta_clave_en_produccion"