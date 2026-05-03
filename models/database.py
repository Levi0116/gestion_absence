# models/database.py - VERSION CORRIGÉE COMPLÈTE

import mysql.connector
from mysql.connector import Error
from config import Config

class Database:
    def __init__(self):
        self.config = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DATABASE,  # IMPORTANT : Spécifier la base
            'port': Config.MYSQL_PORT,
            'charset': 'utf8mb4',
            'use_pure': True,
            'autocommit': True,
            'connection_timeout': 10,
            'raise_on_warnings': True
        }
    
    def get_connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            print(f"❌ Erreur de connexion: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=False):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                result = cursor.lastrowid
                return result
        except Error as e:
            print(f"❌ Erreur d'exécution: {e}")
            return None
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
        return self.db.execute_query(query, fetch=True)
    
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
        return self.db.execute_query(query, fetch=True)
    
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
        return self.db.execute_query(query, fetch=True)
    
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
        result = self.db.execute_query(query, fetch=True)
        return result
    
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
        return self.db.execute_query(query, fetch=True)
    
    def create(self, code_filiere, code_matiere, volume_horaire):
        query = "INSERT INTO Correspondre (code_filiere, code_matiere, Volume_horaire) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (code_filiere, code_matiere, volume_horaire))
    
    def delete(self, code_filiere, code_matiere):
        query = "DELETE FROM Correspondre WHERE code_filiere = %s AND code_matiere = %s"
        return self.db.execute_query(query, (code_filiere, code_matiere))
    
    # ============= MODULE 2 - MODÈLES SUPPLÉMENTAIRES =============

class EtudiantModel:
    """Modèle pour la gestion des étudiants"""
    
    def __init__(self):
        self.db = Database()
    
    def get_all(self):
        query = """
            SELECT e.*, f.Libele_filiere 
            FROM ETUDIANT e
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            ORDER BY e.Nom, e.Prenom
        """
        return self.db.execute_query(query, fetch=True)
    
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
        query = """
            SELECT * FROM ETUDIANT 
            WHERE code_filiere = %s
            ORDER BY Nom, Prenom
        """
        return self.db.execute_query(query, (code_filiere,), fetch=True)
    
    def create(self, nom, prenom, sexe, code_filiere):
        query = """
            INSERT INTO ETUDIANT (Nom, Prenom, Sexe, code_filiere) 
            VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_query(query, (nom, prenom, sexe, code_filiere))
    
    def update(self, id_etudiant, nom, prenom, sexe, code_filiere):
        query = """
            UPDATE ETUDIANT 
            SET Nom = %s, Prenom = %s, Sexe = %s, code_filiere = %s 
            WHERE id_etudiant = %s
        """
        return self.db.execute_query(query, (nom, prenom, sexe, code_filiere, id_etudiant))
    
    def delete(self, id_etudiant):
        query = "DELETE FROM ETUDIANT WHERE id_etudiant = %s"
        return self.db.execute_query(query, (id_etudiant,))
    
    def get_absences_stats(self, id_etudiant):
        query = """
            SELECT 
                COUNT(*) as total_seances,
                SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) as absences,
                SUM(CASE WHEN a.presence = 'J' THEN 1 ELSE 0 END) as justifiees,
                SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) as presences
            FROM Assister a
            WHERE a.id_etudiant = %s
        """
        result = self.db.execute_query(query, (id_etudiant,), fetch=True)
        return result[0] if result else None
    
    def count_all(self):
        query = "SELECT COUNT(*) as total FROM ETUDIANT"
        result = self.db.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0


class EnseignementModel:
    """Modèle pour la gestion des enseignements (séances)"""
    
    def __init__(self):
        self.db = Database()
    
    def get_all(self):
        query = """
            SELECT e.*, 
                   en.Nom as nom_enseignant, en.Prenom as prenom_enseignant,
                   f.Libele_filiere,
                   m.Nom_matiere,
                   p.Libelle_periode
            FROM ENSEIGNEMENT e
            JOIN ENSEIGNANT en ON e.id_enseignant = en.id_enseignant
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            JOIN MATIERE m ON e.code_matiere = m.code_matiere
            JOIN PERIODE p ON e.id_periode = p.id_periode
            ORDER BY e.Date_enseignement DESC, e.Horaire_debut
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_by_id(self, id_enseignement):
        query = """
            SELECT e.*, 
                   en.Nom as nom_enseignant, en.Prenom as prenom_enseignant,
                   f.Libele_filiere,
                   m.Nom_matiere,
                   p.Libelle_periode
            FROM ENSEIGNEMENT e
            JOIN ENSEIGNANT en ON e.id_enseignant = en.id_enseignant
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            JOIN MATIERE m ON e.code_matiere = m.code_matiere
            JOIN PERIODE p ON e.id_periode = p.id_periode
            WHERE e.id_enseignement = %s
        """
        result = self.db.execute_query(query, (id_enseignement,), fetch=True)
        return result[0] if result else None
    
    def get_by_filiere(self, code_filiere):
        query = """
            SELECT e.*, 
                   en.Nom as nom_enseignant, en.Prenom as prenom_enseignant,
                   m.Nom_matiere,
                   p.Libelle_periode
            FROM ENSEIGNEMENT e
            JOIN ENSEIGNANT en ON e.id_enseignant = en.id_enseignant
            JOIN MATIERE m ON e.code_matiere = m.code_matiere
            JOIN PERIODE p ON e.id_periode = p.id_periode
            WHERE e.code_filiere = %s
            ORDER BY e.Date_enseignement DESC
        """
        return self.db.execute_query(query, (code_filiere,), fetch=True)
    
    def create(self, date_enseignement, horaire_debut, horaire_fin, 
               id_enseignant, code_filiere, id_periode, code_matiere):
        query = """
            INSERT INTO ENSEIGNEMENT 
            (Date_enseignement, Horaire_debut, Horaire_fin, 
             id_enseignant, code_filiere, id_periode, code_matiere) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (
            date_enseignement, horaire_debut, horaire_fin,
            id_enseignant, code_filiere, id_periode, code_matiere
        ))
    
    def update(self, id_enseignement, date_enseignement, horaire_debut, horaire_fin,
               id_enseignant, code_filiere, id_periode, code_matiere):
        query = """
            UPDATE ENSEIGNEMENT 
            SET Date_enseignement = %s, Horaire_debut = %s, Horaire_fin = %s,
                id_enseignant = %s, code_filiere = %s, id_periode = %s, code_matiere = %s
            WHERE id_enseignement = %s
        """
        return self.db.execute_query(query, (
            date_enseignement, horaire_debut, horaire_fin,
            id_enseignant, code_filiere, id_periode, code_matiere, id_enseignement
        ))
    
    def delete(self, id_enseignement):
        query = "DELETE FROM ENSEIGNEMENT WHERE id_enseignement = %s"
        return self.db.execute_query(query, (id_enseignement,))
    
    def get_presences(self, id_enseignement):
        query = """
            SELECT e.id_etudiant, e.Nom, e.Prenom, e.Sexe,
                   COALESCE(a.presence, 'A') as presence,
                   a.date_enregistrement
            FROM ETUDIANT e
            LEFT JOIN Assister a ON e.id_etudiant = a.id_etudiant 
                AND a.id_enseignement = %s
            WHERE e.code_filiere = (
                SELECT code_filiere FROM ENSEIGNEMENT WHERE id_enseignement = %s
            )
            ORDER BY e.Nom, e.Prenom
        """
        return self.db.execute_query(query, (id_enseignement, id_enseignement), fetch=True)
    
    def count_all(self):
        query = "SELECT COUNT(*) as total FROM ENSEIGNEMENT"
        result = self.db.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0


class AssisterModel:
    """Modèle pour la gestion des présences/absences"""
    
    def __init__(self):
        self.db = Database()
    
    def save_presences(self, id_enseignement, presences_dict):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            for id_etudiant, presence in presences_dict.items():
                query = """
                    INSERT INTO Assister (id_etudiant, id_enseignement, presence) 
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE presence = %s
                """
                cursor.execute(query, (id_etudiant, id_enseignement, presence, presence))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Erreur sauvegarde présences: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_absences_by_etudiant(self, id_etudiant):
        query = """
            SELECT a.*, 
                   e.Date_enseignement, e.Horaire_debut, e.Horaire_fin,
                   m.Nom_matiere,
                   en.Nom as nom_enseignant, en.Prenom as prenom_enseignant
            FROM Assister a
            JOIN ENSEIGNEMENT e ON a.id_enseignement = e.id_enseignement
            JOIN MATIERE m ON e.code_matiere = m.code_matiere
            JOIN ENSEIGNANT en ON e.id_enseignant = en.id_enseignant
            WHERE a.id_etudiant = %s AND a.presence IN ('A', 'J')
            ORDER BY e.Date_enseignement DESC
        """
        return self.db.execute_query(query, (id_etudiant,), fetch=True)
    
    def justifier_absence(self, id_etudiant, id_enseignement, motif):
        query = """
            UPDATE Assister 
            SET presence = 'J', motif_justification = %s, date_justification = NOW()
            WHERE id_etudiant = %s AND id_enseignement = %s
        """
        return self.db.execute_query(query, (motif, id_etudiant, id_enseignement))
    
    def get_absences_non_justifiees(self, id_etudiant=None, code_filiere=None):
        query = """
            SELECT a.*, 
                   e.id_etudiant, e.Nom, e.Prenom,
                   f.Libele_filiere,
                   ens.Date_enseignement, ens.Horaire_debut, ens.Horaire_fin,
                   m.Nom_matiere,
                   ens.id_enseignement
            FROM Assister a
            JOIN ETUDIANT e ON a.id_etudiant = e.id_etudiant
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            JOIN ENSEIGNEMENT ens ON a.id_enseignement = ens.id_enseignement
            JOIN MATIERE m ON ens.code_matiere = m.code_matiere
            WHERE a.presence = 'A'
        """
        params = []
        if id_etudiant:
            query += " AND e.id_etudiant = %s"
            params.append(id_etudiant)
        if code_filiere:
            query += " AND e.code_filiere = %s"
            params.append(code_filiere)
        
        query += " ORDER BY ens.Date_enseignement DESC"
        return self.db.execute_query(query, tuple(params) if params else None, fetch=True)
    
    def get_statistiques_globales(self):
        query = """
            SELECT 
                f.code_filiere,
                f.Libele_filiere,
                COUNT(DISTINCT e.id_etudiant) as nb_etudiants,
                COUNT(DISTINCT a.id_enseignement) as total_seances,
                SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) as absences_non_justifiees,
                SUM(CASE WHEN a.presence = 'J' THEN 1 ELSE 0 END) as absences_justifiees,
                SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) as presences
            FROM FILIERE f
            LEFT JOIN ETUDIANT e ON f.code_filiere = e.code_filiere
            LEFT JOIN Assister a ON e.id_etudiant = a.id_etudiant
            GROUP BY f.code_filiere, f.Libele_filiere
            ORDER BY f.Libele_filiere
        """
        return self.db.execute_query(query, fetch=True)
    
    def count_absences_non_justifiees(self):
        query = "SELECT COUNT(*) as total FROM Assister WHERE presence = 'A'"
        result = self.db.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0


class MessageModel:
    """Modèle pour l'envoi de messages/notifications"""
    
    def __init__(self):
        self.db = Database()
    
    def get_etudiant_contact(self, id_etudiant):
        query = """
            SELECT e.Nom, e.Prenom, f.Libele_filiere
            FROM ETUDIANT e
            JOIN FILIERE f ON e.code_filiere = f.code_filiere
            WHERE e.id_etudiant = %s
        """
        result = self.db.execute_query(query, (id_etudiant,), fetch=True)
        return result[0] if result else None
    
    def generer_message_absence(self, id_etudiant, absences):
        etudiant = self.get_etudiant_contact(id_etudiant)
        if not etudiant:
            return None
        
        message = f"""
=== NOTIFICATION D'ABSENCES ===

Étudiant(e) : {etudiant['Prenom']} {etudiant['Nom']}
Filière : {etudiant['Libele_filiere']}

Absences enregistrées :
"""
        total_heures = 0
        for absence in absences:
            duree = 2
            total_heures += duree
            
            message += f"""
- {absence['Date_enseignement']} : {absence['Nom_matiere']}
  Statut : {'Justifiée' if absence['presence'] == 'J' else 'Non justifiée'}
"""
        
        penalite = total_heures * 0.1
        message += f"""
Total des heures d'absence : {total_heures:.1f} heures
Pénalité estimée : -{penalite:.2f} points

Veuillez régulariser votre situation.
"""
        return message
    
    
# ============= MODULE 3 - MODÈLES DE RAPPORTS =============

class RapportModel:
    """Modèle pour les rapports et consultations avancées"""
    
    def __init__(self):
        self.db = Database()
    
    def get_matieres_par_filiere(self, code_filiere=None):
        """Récupère les matières par filière avec détails"""
        query = """
            SELECT 
                f.code_filiere,
                f.Libele_filiere,
                f.Nbre_etudiant,
                m.code_matiere,
                m.Nom_matiere,
                c.Volume_horaire,
                COUNT(DISTINCT ens.id_enseignement) as nb_seances,
                (
                    SELECT COUNT(DISTINCT a.id_enseignement)
                    FROM Assister a
                    JOIN ENSEIGNEMENT ens2 ON a.id_enseignement = ens2.id_enseignement
                    WHERE ens2.code_filiere = f.code_filiere 
                    AND ens2.code_matiere = m.code_matiere
                    AND a.presence = 'A'
                ) as nb_absences,
                (
                    SELECT COUNT(DISTINCT a.id_enseignement)
                    FROM Assister a
                    JOIN ENSEIGNEMENT ens2 ON a.id_enseignement = ens2.id_enseignement
                    WHERE ens2.code_filiere = f.code_filiere 
                    AND ens2.code_matiere = m.code_matiere
                    AND a.presence = 'J'
                ) as nb_justifiees
            FROM FILIERE f
            JOIN Correspondre c ON f.code_filiere = c.code_filiere
            JOIN MATIERE m ON c.code_matiere = m.code_matiere
            LEFT JOIN ENSEIGNEMENT ens ON f.code_filiere = ens.code_filiere 
                AND m.code_matiere = ens.code_matiere
        """
        params = []
        if code_filiere:
            query += " WHERE f.code_filiere = %s"
            params.append(code_filiere)
        
        query += " GROUP BY f.code_filiere, f.Libele_filiere, f.Nbre_etudiant, m.code_matiere, m.Nom_matiere, c.Volume_horaire"
        query += " ORDER BY f.Libele_filiere, m.Nom_matiere"
        
        return self.db.execute_query(query, tuple(params) if params else None, fetch=True)
    
    def get_absences_par_filiere_periode(self, code_filiere=None, id_periode=None):
        """Récupère les absences par filière et par période"""
        query = """
            SELECT 
                f.code_filiere,
                f.Libele_filiere,
                p.id_periode,
                p.Libelle_periode,
                p.Date_debut,
                p.Date_fin,
                COUNT(DISTINCT e.id_etudiant) as nb_etudiants,
                COUNT(DISTINCT ens.id_enseignement) as nb_seances,
                SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) as nb_presences,
                SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) as nb_absences,
                SUM(CASE WHEN a.presence = 'J' THEN 1 ELSE 0 END) as nb_justifiees,
                ROUND(
                    SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) * 100.0 / 
                    NULLIF(COUNT(a.id_enseignement), 0), 1
                ) as taux_presence,
                ROUND(
                    SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) * 100.0 / 
                    NULLIF(COUNT(a.id_enseignement), 0), 1
                ) as taux_absence
            FROM FILIERE f
            LEFT JOIN ETUDIANT e ON f.code_filiere = e.code_filiere
            LEFT JOIN ENSEIGNEMENT ens ON f.code_filiere = ens.code_filiere
            LEFT JOIN PERIODE p ON ens.id_periode = p.id_periode
            LEFT JOIN Assister a ON ens.id_enseignement = a.id_enseignement 
                AND e.id_etudiant = a.id_etudiant
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
        
        return self.db.execute_query(query, tuple(params) if params else None, fetch=True)
    
    def get_absences_par_etudiant(self, id_etudiant=None, code_filiere=None, id_periode=None):
        """Récupère les absences détaillées par étudiant"""
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
                ROUND(
                    SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) * 0.1, 2
                ) as penalite,
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
        
        return self.db.execute_query(query, tuple(params) if params else None, fetch=True)
    
    def get_absences_justifiees(self, code_filiere=None, id_periode=None):
        """Récupère la liste des absences justifiées"""
        query = """
            SELECT 
                e.id_etudiant,
                e.Nom,
                e.Prenom,
                f.Libele_filiere,
                ens.Date_enseignement,
                ens.Horaire_debut,
                ens.Horaire_fin,
                m.Nom_matiere,
                a.presence,
                a.motif_justification,
                a.date_justification,
                en.Nom as nom_enseignant,
                en.Prenom as prenom_enseignant,
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
        
        # CORRECTION : Retourner une liste vide si aucun résultat
        
        result = self.db.execute_query(query, tuple(params) if params else None, fetch=True)
        return result if result is not None else []
    
    def get_detail_etudiant(self, id_etudiant):
        """Récupère le détail complet des absences d'un étudiant"""
        query = """
            SELECT 
                ens.Date_enseignement,
                ens.Horaire_debut,
                ens.Horaire_fin,
                m.Nom_matiere,
                a.presence,
                a.motif_justification,
                a.date_justification,
                a.date_enregistrement,
                en.Nom as nom_enseignant,
                en.Prenom as prenom_enseignant,
                p.Libelle_periode,
                f.Libele_filiere
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
        return self.db.execute_query(query, (id_etudiant,), fetch=True)
    
    def get_resume_etudiant(self, id_etudiant):
        """Récupère le résumé des absences par matière pour un étudiant"""
        query = """
            SELECT 
                m.Nom_matiere,
                COUNT(DISTINCT ens.id_enseignement) as nb_seances,
                SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) as nb_presences,
                SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) as nb_absences,
                SUM(CASE WHEN a.presence = 'J' THEN 1 ELSE 0 END) as nb_justifiees,
                ROUND(
                    SUM(CASE WHEN a.presence = 'A' THEN 1 ELSE 0 END) * 0.1, 2
                ) as penalite
            FROM Assister a
            JOIN ENSEIGNEMENT ens ON a.id_enseignement = ens.id_enseignement
            JOIN MATIERE m ON ens.code_matiere = m.code_matiere
            WHERE a.id_etudiant = %s
            GROUP BY m.Nom_matiere
            ORDER BY nb_absences DESC, m.Nom_matiere
        """
        return self.db.execute_query(query, (id_etudiant,), fetch=True)
    
    def get_statistiques_avancees(self):
        """Statistiques avancées globales"""
        query = """
            SELECT 
                (SELECT COUNT(*) FROM ETUDIANT) as total_etudiants,
                (SELECT COUNT(*) FROM ENSEIGNEMENT) as total_seances,
                (SELECT COUNT(*) FROM Assister WHERE presence = 'A') as total_absences,
                (SELECT COUNT(*) FROM Assister WHERE presence = 'J') as total_justifiees,
                (SELECT COUNT(*) FROM Assister WHERE presence = 'P') as total_presences,
                (
                    SELECT ROUND(AVG(taux), 1) FROM (
                        SELECT 
                            SUM(CASE WHEN a.presence = 'P' THEN 1 ELSE 0 END) * 100.0 / 
                            NULLIF(COUNT(a.id_enseignement), 0) as taux
                        FROM ETUDIANT e
                        LEFT JOIN Assister a ON e.id_etudiant = a.id_etudiant
                        GROUP BY e.id_etudiant
                        HAVING COUNT(a.id_enseignement) > 0
                    ) as subquery
                ) as taux_presence_moyen,
                (
                    SELECT f.Libele_filiere
                    FROM FILIERE f
                    JOIN ETUDIANT e ON f.code_filiere = e.code_filiere
                    JOIN Assister a ON e.id_etudiant = a.id_etudiant
                    WHERE a.presence = 'A'
                    GROUP BY f.code_filiere, f.Libele_filiere
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                ) as filiere_plus_absenteiste
        """
        result = self.db.execute_query(query, fetch=True)
        return result[0] if result else None