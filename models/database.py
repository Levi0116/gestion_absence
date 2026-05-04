# models/database.py - VERSION RAILWAY CORRIGÉE

import mysql.connector
from mysql.connector import Error
from config import Config
import os
import sys

class Database:
    def __init__(self):
        self.config = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DATABASE,
            'port': Config.MYSQL_PORT,
            'charset': 'utf8mb4',
            'use_pure': True,
            'autocommit': True,
            'connection_timeout': 10,
        }

    def get_connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            print(f"❌ Erreur de connexion MySQL: {e}")
            return None

    def execute_query(self, query, params=None, fetch=False):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            if not conn:
                # Retourner liste vide ou None selon le contexte
                return [] if fetch else None

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if fetch:
                result = cursor.fetchall()
                return result if result is not None else []
            else:
                conn.commit()
                return cursor.lastrowid

        except Error as e:
            print(f"❌ Erreur d'exécution: {e}")
            return [] if fetch else None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


class PeriodeModel:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = "SELECT * FROM PERIODE ORDER BY Date_debut DESC"
        return self.db.execute_query(query, fetch=True) or []

    def get_by_id(self, id_periode):
        query = "SELECT * FROM PERIODE WHERE id_periode = %s"
        result = self.db.execute_query(query, (id_periode,), fetch=True)
        return result[0] if result else None

    def create(self, libelle, date_debut, date_fin):
        query = "INSERT INTO PERIODE (Libelle_periode, Date_debut, Date_fin) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (libelle, date_debut, date_fin))

    def update(self, id_periode, libelle, date_debut, date_fin):
        query = "UPDATE PERIODE SET Libelle_periode = %s, Date_debut = %s, Date_fin = %s WHERE id_periode = %s"
        return self.db.execute_query(query, (libelle, date_debut, date_fin, id_periode))

    def delete(self, id_periode):
        query = "DELETE FROM PERIODE WHERE id_periode = %s"
        return self.db.execute_query(query, (id_periode,))


class MatiereModel:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = "SELECT * FROM MATIERE ORDER BY Nom_matiere"
        return self.db.execute_query(query, fetch=True) or []

    def get_by_id(self, code_matiere):
        query = "SELECT * FROM MATIERE WHERE code_matiere = %s"
        result = self.db.execute_query(query, (code_matiere,), fetch=True)
        return result[0] if result else None

    def create(self, nom_matiere):
        query = "INSERT INTO MATIERE (Nom_matiere) VALUES (%s)"
        return self.db.execute_query(query, (nom_matiere,))

    def update(self, code_matiere, nom_matiere):
        query = "UPDATE MATIERE SET Nom_matiere = %s WHERE code_matiere = %s"
        return self.db.execute_query(query, (nom_matiere, code_matiere))

    def delete(self, code_matiere):
        query = "DELETE FROM MATIERE WHERE code_matiere = %s"
        return self.db.execute_query(query, (code_matiere,))


class EnseignantModel:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = "SELECT * FROM ENSEIGNANT ORDER BY Nom, Prenom"
        return self.db.execute_query(query, fetch=True) or []

    def get_by_id(self, id_enseignant):
        query = "SELECT * FROM ENSEIGNANT WHERE id_enseignant = %s"
        result = self.db.execute_query(query, (id_enseignant,), fetch=True)
        return result[0] if result else None

    def create(self, nom, prenom, mail, specialite, diplome, sexe):
        query = """INSERT INTO ENSEIGNANT (Nom, Prenom, Mail, Specialite, Diplome, Sexe)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        return self.db.execute_query(query, (nom, prenom, mail, specialite, diplome, sexe))

    def update(self, id_enseignant, nom, prenom, mail, specialite, diplome, sexe):
        query = """UPDATE ENSEIGNANT
                   SET Nom = %s, Prenom = %s, Mail = %s, Specialite = %s, Diplome = %s, Sexe = %s
                   WHERE id_enseignant = %s"""
        return self.db.execute_query(query, (nom, prenom, mail, specialite, diplome, sexe, id_enseignant))

    def delete(self, id_enseignant):
        query = "DELETE FROM ENSEIGNANT WHERE id_enseignant = %s"
        return self.db.execute_query(query, (id_enseignant,))


class FiliereModel:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = "SELECT * FROM FILIERE ORDER BY Libele_filiere"
        return self.db.execute_query(query, fetch=True) or []

    def get_by_id(self, code_filiere):
        query = "SELECT * FROM FILIERE WHERE code_filiere = %s"
        result = self.db.execute_query(query, (code_filiere,), fetch=True)
        return result[0] if result else None

    def create(self, libelle, nbre_etudiant):
        query = "INSERT INTO FILIERE (Libele_filiere, Nbre_etudiant) VALUES (%s, %s)"
        return self.db.execute_query(query, (libelle, nbre_etudiant))

    def update(self, code_filiere, libelle, nbre_etudiant):
        query = "UPDATE FILIERE SET Libele_filiere = %s, Nbre_etudiant = %s WHERE code_filiere = %s"
        return self.db.execute_query(query, (libelle, nbre_etudiant, code_filiere))

    def delete(self, code_filiere):
        query = "DELETE FROM FILIERE WHERE code_filiere = %s"
        return self.db.execute_query(query, (code_filiere,))


class CorrespondreModel:
    def __init__(self):
        self.db = Database()

    def get_all_with_names(self):
        query = """
            SELECT c.*, f.Libele_filiere, m.Nom_matiere
            FROM Correspondre c
            JOIN FILIERE f ON c.code_filiere = f.code_filiere
            JOIN MATIERE m ON c.code_matiere = m.code_matiere
            ORDER BY f.Libele_filiere, m.Nom_matiere
        """
        return self.db.execute_query(query, fetch=True) or []

    def create(self, code_filiere, code_matiere, volume_horaire):
        query = "INSERT INTO Correspondre (code_filiere, code_matiere, Volume_horaire) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (code_filiere, code_matiere, volume_horaire))

    def delete(self, code_filiere, code_matiere):
        query = "DELETE FROM Correspondre WHERE code_filiere = %s AND code_matiere = %s"
        return self.db.execute_query(query, (code_filiere, code_matiere))


class EtudiantModel:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = """
            SELECT e.*, f.Libele_filiere
            FROM ETUDIANT e
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            ORDER BY e.Nom, e.Prenom
        """
        return self.db.execute_query(query, fetch=True) or []

    def get_by_id(self, id_etudiant):
        query = """
            SELECT e.*, f.Libele_filiere
            FROM ETUDIANT e
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            WHERE e.id_etudiant = %s
        """
        result = self.db.execute_query(query, (id_etudiant,), fetch=True)
        return result[0] if result else None

    def get_by_filiere(self, code_filiere):
        query = "SELECT * FROM ETUDIANT WHERE code_filiere = %s ORDER BY Nom, Prenom"
        return self.db.execute_query(query, (code_filiere,), fetch=True) or []

    def count_all(self):
        query = "SELECT COUNT(*) as total FROM ETUDIANT"
        result = self.db.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0

    def create(self, nom, prenom, sexe, code_filiere):
        query = "INSERT INTO ETUDIANT (Nom, Prenom, Sexe, code_filiere) VALUES (%s, %s, %s, %s)"
        return self.db.execute_query(query, (nom, prenom, sexe, code_filiere))

    def update(self, id_etudiant, nom, prenom, sexe, code_filiere):
        query = "UPDATE ETUDIANT SET Nom = %s, Prenom = %s, Sexe = %s, code_filiere = %s WHERE id_etudiant = %s"
        return self.db.execute_query(query, (nom, prenom, sexe, code_filiere, id_etudiant))

    def delete(self, id_etudiant):
        query = "DELETE FROM ETUDIANT WHERE id_etudiant = %s"
        return self.db.execute_query(query, (id_etudiant,))


class EnseignementModel:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = """
            SELECT ens.*, e.Nom as nom_enseignant, e.Prenom as prenom_enseignant,
                   f.Libele_filiere, p.Libelle_periode, m.Nom_matiere
            FROM ENSEIGNEMENT ens
            JOIN ENSEIGNANT e ON ens.id_enseignant = e.id_enseignant
            JOIN FILIERE f ON ens.code_filiere = f.code_filiere
            JOIN PERIODE p ON ens.id_periode = p.id_periode
            JOIN MATIERE m ON ens.code_matiere = m.code_matiere
            ORDER BY ens.Date_enseignement DESC
        """
        return self.db.execute_query(query, fetch=True) or []

    def get_by_id(self, id_enseignement):
        query = """
            SELECT ens.*, e.Nom as nom_enseignant, e.Prenom as prenom_enseignant,
                   f.Libele_filiere, p.Libelle_periode, m.Nom_matiere
            FROM ENSEIGNEMENT ens
            JOIN ENSEIGNANT e ON ens.id_enseignant = e.id_enseignant
            JOIN FILIERE f ON ens.code_filiere = f.code_filiere
            JOIN PERIODE p ON ens.id_periode = p.id_periode
            JOIN MATIERE m ON ens.code_matiere = m.code_matiere
            WHERE ens.id_enseignement = %s
        """
        result = self.db.execute_query(query, (id_enseignement,), fetch=True)
        return result[0] if result else None

    def count_all(self):
        query = "SELECT COUNT(*) as total FROM ENSEIGNEMENT"
        result = self.db.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0

    def create(self, date_enseignement, horaire_debut, horaire_fin, id_enseignant, code_filiere, id_periode, code_matiere):
        query = """INSERT INTO ENSEIGNEMENT
                   (Date_enseignement, Horaire_debut, Horaire_fin, id_enseignant, code_filiere, id_periode, code_matiere)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        return self.db.execute_query(query, (date_enseignement, horaire_debut, horaire_fin,
                                              id_enseignant, code_filiere, id_periode, code_matiere))

    def update(self, id_enseignement, date_enseignement, horaire_debut, horaire_fin,
               id_enseignant, code_filiere, id_periode, code_matiere):
        query = """UPDATE ENSEIGNEMENT
                   SET Date_enseignement = %s, Horaire_debut = %s, Horaire_fin = %s,
                       id_enseignant = %s, code_filiere = %s, id_periode = %s, code_matiere = %s
                   WHERE id_enseignement = %s"""
        return self.db.execute_query(query, (date_enseignement, horaire_debut, horaire_fin,
                                              id_enseignant, code_filiere, id_periode,
                                              code_matiere, id_enseignement))

    def delete(self, id_enseignement):
        query = "DELETE FROM ENSEIGNEMENT WHERE id_enseignement = %s"
        return self.db.execute_query(query, (id_enseignement,))


class AssisterModel:
    def __init__(self):
        self.db = Database()

    def get_by_enseignement(self, id_enseignement):
        query = """
            SELECT a.*, e.Nom, e.Prenom, e.Sexe, f.Libele_filiere
            FROM Assister a
            JOIN ETUDIANT e ON a.id_etudiant = e.id_etudiant
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            WHERE a.id_enseignement = %s
            ORDER BY e.Nom, e.Prenom
        """
        return self.db.execute_query(query, (id_enseignement,), fetch=True) or []

    def count_absences_non_justifiees(self):
        query = "SELECT COUNT(*) as total FROM Assister WHERE presence = 'A'"
        result = self.db.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0

    def update_presence(self, id_etudiant, id_enseignement, presence,
                        motif=None, date_justification=None):
        query = """UPDATE Assister
                   SET presence = %s, motif_justification = %s, date_justification = %s
                   WHERE id_etudiant = %s AND id_enseignement = %s"""
        return self.db.execute_query(query, (presence, motif, date_justification,
                                              id_etudiant, id_enseignement))

    def insert_or_update(self, id_etudiant, id_enseignement, presence):
        query = """INSERT INTO Assister (id_etudiant, id_enseignement, presence)
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE presence = %s"""
        return self.db.execute_query(query, (id_etudiant, id_enseignement, presence, presence))

    def get_statistiques_globales(self):
        query = """
            SELECT
                COUNT(*) as total_enregistrements,
                SUM(CASE WHEN presence = 'P' THEN 1 ELSE 0 END) as total_presences,
                SUM(CASE WHEN presence = 'A' THEN 1 ELSE 0 END) as total_absences,
                SUM(CASE WHEN presence = 'J' THEN 1 ELSE 0 END) as total_justifiees
            FROM Assister
        """
        result = self.db.execute_query(query, fetch=True)
        return result[0] if result else {
            'total_enregistrements': 0,
            'total_presences': 0,
            'total_absences': 0,
            'total_justifiees': 0
        }


class MessageModel:
    def __init__(self):
        self.db = Database()

    def create(self, contenu, id_enseignant=None, id_etudiant=None):
        query = """INSERT INTO Message (contenu, id_enseignant, id_etudiant)
                   VALUES (%s, %s, %s)"""
        return self.db.execute_query(query, (contenu, id_enseignant, id_etudiant))

    def get_all(self):
        query = "SELECT * FROM Message ORDER BY date_envoi DESC"
        return self.db.execute_query(query, fetch=True) or []


class RapportModel:
    def __init__(self):
        self.db = Database()

    def get_matieres_par_filiere(self, code_filiere=None):
        query = """
            SELECT
                f.code_filiere,
                f.Libele_filiere,
                f.Nbre_etudiant,
                m.code_matiere,
                m.Nom_matiere,
                c.Volume_horaire
            FROM FILIERE f
            JOIN Correspondre c ON f.code_filiere = c.code_filiere
            JOIN MATIERE m ON c.code_matiere = m.code_matiere
        """
        params = []
        if code_filiere:
            query += " WHERE f.code_filiere = %s"
            params.append(code_filiere)
        query += " ORDER BY f.Libele_filiere, m.Nom_matiere"
        return self.db.execute_query(query, tuple(params) if params else None, fetch=True) or []

    def get_absences_par_filiere_periode(self, code_filiere=None, id_periode=None):
        query = """
            SELECT
                f.Libele_filiere,
                p.Libelle_periode,
                p.Date_debut,
                p.Date_fin,
                COUNT(DISTINCT ens.id_enseignement) as nb_seances,
                COUNT(DISTINCT e.id_etudiant) as nb_etudiants,
                SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) as total_absences,
                SUM(CASE WHEN a.presence = 'J' THEN 1 ELSE 0 END) as total_justifiees,
                SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) as total_presences
            FROM FILIERE f
            JOIN ETUDIANT e ON f.code_filiere = e.code_filiere
            JOIN Assister a ON e.id_etudiant = a.id_etudiant
            JOIN ENSEIGNEMENT ens ON a.id_enseignement = ens.id_enseignement
            JOIN PERIODE p ON ens.id_periode = p.id_periode
        """
        conditions = []
        params = []
        if code_filiere:
            conditions.append("f.code_filiere = %s")
            params.append(code_filiere)
        if id_periode:
            conditions.append("p.id_periode = %s")
            params.append(id_periode)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += """
            GROUP BY f.code_filiere, f.Libele_filiere, p.id_periode,
                     p.Libelle_periode, p.Date_debut, p.Date_fin
            ORDER BY f.Libele_filiere, p.Date_debut DESC
        """
        return self.db.execute_query(query, tuple(params) if params else None, fetch=True) or []

    def get_absences_par_etudiant(self, id_etudiant=None, code_filiere=None, id_periode=None):
        query = """
            SELECT
                e.id_etudiant,
                e.Nom,
                e.Prenom,
                e.Sexe,
                f.Libele_filiere,
                COUNT(DISTINCT a.id_enseignement) as total_seances,
                SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) as nb_presences,
                SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) as nb_absences,
                SUM(CASE WHEN a.presence = 'J' THEN 1 ELSE 0 END) as nb_justifiees,
                ROUND(SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) * 0.1, 2) as penalite,
                ROUND(
                    SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) * 100.0 /
                    NULLIF(COUNT(DISTINCT a.id_enseignement), 0), 1
                ) as taux_presence
            FROM ETUDIANT e
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            LEFT JOIN Assister a ON e.id_etudiant = a.id_etudiant
            LEFT JOIN ENSEIGNEMENT ens ON a.id_enseignement = ens.id_enseignement
        """
        conditions = []
        params = []
        if id_etudiant:
            conditions.append("e.id_etudiant = %s")
            params.append(id_etudiant)
        if code_filiere:
            conditions.append("e.code_filiere = %s")
            params.append(code_filiere)
        if id_periode:
            conditions.append("ens.id_periode = %s")
            params.append(id_periode)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += """
            GROUP BY e.id_etudiant, e.Nom, e.Prenom, e.Sexe, f.Libele_filiere
            ORDER BY nb_absences DESC, e.Nom, e.Prenom
        """
        return self.db.execute_query(query, tuple(params) if params else None, fetch=True) or []

    def get_absences_justifiees(self, code_filiere=None, id_periode=None):
        query = """
            SELECT
                e.id_etudiant, e.Nom, e.Prenom,
                f.Libele_filiere,
                ens.Date_enseignement, ens.Horaire_debut, ens.Horaire_fin,
                m.Nom_matiere,
                a.presence, a.motif_justification, a.date_justification,
                en.Nom as nom_enseignant, en.Prenom as prenom_enseignant,
                p.Libelle_periode
            FROM Assister a
            JOIN ETUDIANT e ON a.id_etudiant = e.id_etudiant
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            JOIN ENSEIGNEMENT ens ON a.id_enseignement = ens.id_enseignement
            JOIN MATIERE m ON ens.code_matiere = m.code_matiere
            JOIN ENSEIGNANT en ON ens.id_enseignant = en.id_enseignant
            JOIN PERIODE p ON ens.id_periode = p.id_periode
            WHERE a.presence = 'J'
        """
        conditions = []
        params = []
        if code_filiere:
            conditions.append("e.code_filiere = %s")
            params.append(code_filiere)
        if id_periode:
            conditions.append("ens.id_periode = %s")
            params.append(id_periode)
        if conditions:
            query += " AND " + " AND ".join(conditions)
        query += " ORDER BY ens.Date_enseignement DESC, e.Nom, e.Prenom"
        result = self.db.execute_query(query, tuple(params) if params else None, fetch=True)
        return result if result is not None else []

    def get_detail_etudiant(self, id_etudiant):
        query = """
            SELECT
                ens.Date_enseignement, ens.Horaire_debut, ens.Horaire_fin,
                m.Nom_matiere, a.presence, a.motif_justification, a.date_justification,
                a.date_enregistrement, en.Nom as nom_enseignant, en.Prenom as prenom_enseignant,
                p.Libelle_periode, f.Libele_filiere
            FROM Assister a
            JOIN ENSEIGNEMENT ens ON a.id_enseignement = ens.id_enseignement
            JOIN MATIERE m ON ens.code_matiere = m.code_matiere
            JOIN ENSEIGNANT en ON ens.id_enseignant = en.id_enseignant
            JOIN PERIODE p ON ens.id_periode = p.id_periode
            JOIN ETUDIANT e ON a.id_etudiant = e.id_etudiant
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            WHERE a.id_etudiant = %s
            ORDER BY ens.Date_enseignement DESC, ens.Horaire_debut
        """
        return self.db.execute_query(query, (id_etudiant,), fetch=True) or []

    def get_resume_etudiant(self, id_etudiant):
        query = """
            SELECT
                m.Nom_matiere,
                COUNT(DISTINCT ens.id_enseignement) as nb_seances,
                SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) as nb_presences,
                SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) as nb_absences,
                SUM(CASE WHEN a.presence = 'J' THEN 1 ELSE 0 END) as nb_justifiees,
                ROUND(SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) * 0.1, 2) as penalite
            FROM Assister a
            JOIN ENSEIGNEMENT ens ON a.id_enseignement = ens.id_enseignement
            JOIN MATIERE m ON ens.code_matiere = m.code_matiere
            WHERE a.id_etudiant = %s
            GROUP BY m.Nom_matiere
            ORDER BY nb_absences DESC, m.Nom_matiere
        """
        return self.db.execute_query(query, (id_etudiant,), fetch=True) or []

    def get_statistiques_avancees(self):
        query = """
            SELECT
                (SELECT COUNT(*) FROM ETUDIANT) as total_etudiants,
                (SELECT COUNT(*) FROM ENSEIGNEMENT) as total_seances,
                (SELECT COUNT(*) FROM Assister WHERE presence = 'A') as total_absences,
                (SELECT COUNT(*) FROM Assister WHERE presence = 'J') as total_justifiees,
                (SELECT COUNT(*) FROM Assister WHERE presence = 'P') as total_presences
        """
        result = self.db.execute_query(query, fetch=True)
        return result[0] if result else {
            'total_etudiants': 0,
            'total_seances': 0,
            'total_absences': 0,
            'total_justifiees': 0,
            'total_presences': 0,
            'taux_presence_moyen': 0,
            'filiere_plus_absenteiste': 'N/A'
        }
