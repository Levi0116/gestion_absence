# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Forcer le rechargement du fichier .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuration MySQL - Forcer la lecture depuis .env
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'gestion_absences')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    
    # Règlement des absences
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