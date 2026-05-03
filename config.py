# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Forcer le rechargement du fichier .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    MYSQL_HOST = os.environ.get('MYSQLHOST', 'mysql.railway.internal')
    MYSQL_USER = os.environ.get('MYSQLUSER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQLDATABASE', 'railway')
    MYSQL_PORT = int(os.environ.get('MYSQLPORT', 3306))

    PENALITE_PAR_HEURE = 0.1
    SEUIL_INVALIDATION_CREDITS = 5
    
    # Afficher la configuration pour déboguer
    @classmethod
    def display_config(cls):
        print(f"📋 Configuration MySQL chargée :")
        print(f"   Host: {cls.MYSQL_HOST}")
        print(f"   User: {cls.MYSQL_USER}")
        print(f"   Database: {cls.MYSQL_DATABASE}")
        print(f"   Port: {cls.MYSQL_PORT}")