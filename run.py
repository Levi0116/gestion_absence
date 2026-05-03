#!/usr/bin/env python
# run.py
"""Script de démarrage rapide pour l'application Flask"""

import os
import sys
import subprocess
import webbrowser
from threading import Timer

def open_browser():
    """Ouvre le navigateur après 1.5 secondes"""
    webbrowser.open_new('http://localhost:5000')

def check_dependencies():
    """Vérifie si les dépendances sont installées"""
    try:
        import flask
        import mysql.connector
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante : {e}")
        print("\n📦 Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès !\n")
        return True

# run.py - Modifier la fonction check_database()

# run.py - Remplacer la fonction check_database()

def check_database():
    """Vérifie la configuration de la base de données"""
    from config import Config
    
    # Afficher la configuration
    Config.display_config()
    
    try:
        import mysql.connector
        
        # Test avec différentes configurations possibles
        configs_to_test = [
            # Configuration depuis .env
            {
                'host': Config.MYSQL_HOST,
                'user': Config.MYSQL_USER,
                'password': Config.MYSQL_PASSWORD,
                'port': Config.MYSQL_PORT,
            },
            # Configuration par défaut XAMPP
            {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'port': 3306,
            },
            # Configuration par défaut MySQL Windows
            {
                'host': '127.0.0.1',
                'user': 'root',
                'password': '',
                'port': 3306,
            }
        ]
        
        connected = False
        conn = None
        
        for cfg in configs_to_test:
            try:
                conn = mysql.connector.connect(
                    host=cfg['host'],
                    user=cfg['user'],
                    password=cfg['password'],
                    port=cfg['port'],
                    connection_timeout=3
                )
                if conn.is_connected():
                    print(f"✅ Connexion réussie avec: host={cfg['host']}, user={cfg['user']}")
                    connected = True
                    break
            except:
                continue
        
        if not connected:
            print("\n❌ Impossible de se connecter à MySQL")
            print("\n📌 Solutions possibles :")
            print("   1. Vérifiez que MySQL/XAMPP est démarré")
            print("   2. Modifiez le fichier .env avec vos identifiants phpMyAdmin")
            print("   3. Dans phpMyAdmin, l'utilisateur par défaut est 'root' sans mot de passe")
            return False
        
        cursor = conn.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{Config.MYSQL_DATABASE}'")
        
        if not cursor.fetchone():
            print(f"⚠️  Base de données '{Config.MYSQL_DATABASE}' non trouvée !")
            print("📝 Création de la base de données...")
            
            # Créer la base de données si elle n'existe pas
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
            print(f"✅ Base de données '{Config.MYSQL_DATABASE}' créée avec succès !")
            
            # Demander si l'utilisateur veut importer le schéma
            print("\n📌 Pour importer les tables, exécutez le script sql/database.sql dans phpMyAdmin")
            print("   Ou importez-le via : mysql -u root -p gestion_absences < sql/database.sql")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("🎓 GESTION DES ABSENCES - MODULE PARAMÉTRAGE")
    print("=" * 50)
    print()
    
    # Vérification des dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Vérification de la base de données
    if not check_database():
        print("\n⚠️  L'application va démarrer mais certaines fonctionnalités peuvent ne pas fonctionner.")
    
    print("\n🚀 Démarrage de l'application Flask...")
    print("📍 Accédez à : http://localhost:5000")
    print("🛑 Appuyez sur Ctrl+C pour arrêter\n")
    
    # Ouvre le navigateur automatiquement
    Timer(1.5, open_browser).start()
    
    # Lance l'application
    from app import app
    app.run(debug=True, port=5000)