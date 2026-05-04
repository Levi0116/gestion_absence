# config.py - Compatible Railway + local
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Railway utilise MYSQLHOST, en local on utilise MYSQL_HOST
    MYSQL_HOST = (
        os.environ.get('MYSQLHOST') or
        os.environ.get('MYSQL_HOST') or
        'localhost'
    )
    MYSQL_USER = (
        os.environ.get('MYSQLUSER') or
        os.environ.get('MYSQL_USER') or
        'root'
    )
    MYSQL_PASSWORD = (
        os.environ.get('MYSQLPASSWORD') or
        os.environ.get('MYSQL_PASSWORD') or
        ''
    )
    MYSQL_DATABASE = (
        os.environ.get('MYSQLDATABASE') or
        os.environ.get('MYSQL_DATABASE') or
        'railway'
    )
    MYSQL_PORT = int(
        os.environ.get('MYSQLPORT') or
        os.environ.get('MYSQL_PORT') or
        3306
    )

    # Règlement des absences
    PENALITE_PAR_HEURE = 0.1
    SEUIL_INVALIDATION_CREDITS = 5
