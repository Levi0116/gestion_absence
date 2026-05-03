-- =====================================================
-- SCRIPT SQL POUR GESTION DES ABSENCES
-- =====================================================

-- Suppression des tables existantes
DROP TABLE IF EXISTS Assister;
DROP TABLE IF EXISTS ENSEIGNEMENT;
DROP TABLE IF EXISTS ETUDIANT;
DROP TABLE IF EXISTS Correspondre;
DROP TABLE IF EXISTS ENSEIGNANT;
DROP TABLE IF EXISTS PERIODE;
DROP TABLE IF EXISTS MATIERE;
DROP TABLE IF EXISTS FILIERE;

-- Table FILIERE
CREATE TABLE FILIERE(
   code_filiere INT AUTO_INCREMENT,
   Libele_filiere VARCHAR(50) NOT NULL,
   Nbre_etudiant INT DEFAULT 0,
   PRIMARY KEY(code_filiere)
);

-- Table MATIERE
CREATE TABLE MATIERE(
   code_matiere INT AUTO_INCREMENT,
   Nom_matiere VARCHAR(50) NOT NULL,
   PRIMARY KEY(code_matiere)
);

-- Table PERIODE
CREATE TABLE PERIODE(
   id_periode INT AUTO_INCREMENT,
   Date_debut DATE NOT NULL,
   Date_fin DATE NOT NULL,
   Libelle_periode VARCHAR(100),
   PRIMARY KEY(id_periode)
);

-- Table ENSEIGNANT
CREATE TABLE ENSEIGNANT(
   id_enseignant INT AUTO_INCREMENT,
   Nom VARCHAR(50) NOT NULL,
   Prenom VARCHAR(50) NOT NULL,
   Mail VARCHAR(100) UNIQUE NOT NULL,
   Specialite VARCHAR(100),
   Diplome VARCHAR(100),
   Sexe ENUM('M', 'F') NOT NULL,
   PRIMARY KEY(id_enseignant)
);

-- Table ETUDIANT
CREATE TABLE ETUDIANT(
   id_etudiant INT AUTO_INCREMENT,
   Nom VARCHAR(50) NOT NULL,
   Prenom VARCHAR(50) NOT NULL,
   Sexe ENUM('M', 'F') NOT NULL,
   code_filiere INT NOT NULL,
   PRIMARY KEY(id_etudiant),
   FOREIGN KEY(code_filiere) REFERENCES FILIERE(code_filiere) ON DELETE CASCADE
);

-- Table ENSEIGNEMENT
CREATE TABLE ENSEIGNEMENT(
   id_enseignement INT AUTO_INCREMENT,
   Date_enseignement DATE NOT NULL,
   Horaire_debut TIME NOT NULL,
   Horaire_fin TIME NOT NULL,
   id_enseignant INT NOT NULL,
   code_filiere INT NOT NULL,
   id_periode INT NOT NULL,
   code_matiere INT NOT NULL,
   PRIMARY KEY(id_enseignement),
   FOREIGN KEY(id_enseignant) REFERENCES ENSEIGNANT(id_enseignant) ON DELETE CASCADE,
   FOREIGN KEY(code_filiere) REFERENCES FILIERE(code_filiere) ON DELETE CASCADE,
   FOREIGN KEY(id_periode) REFERENCES PERIODE(id_periode) ON DELETE CASCADE,
   FOREIGN KEY(code_matiere) REFERENCES MATIERE(code_matiere) ON DELETE CASCADE
);

-- Table Correspondre
CREATE TABLE Correspondre(
   code_filiere INT,
   code_matiere INT,
   Volume_horaire INT NOT NULL,
   PRIMARY KEY(code_filiere, code_matiere),
   FOREIGN KEY(code_filiere) REFERENCES FILIERE(code_filiere) ON DELETE CASCADE,
   FOREIGN KEY(code_matiere) REFERENCES MATIERE(code_matiere) ON DELETE CASCADE
);

-- Table Assister
CREATE TABLE Assister(
   id_etudiant INT,
   id_enseignement INT,
   presence ENUM('P', 'A', 'J') DEFAULT 'A',
   date_enregistrement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(id_etudiant, id_enseignement),
   FOREIGN KEY(id_etudiant) REFERENCES ETUDIANT(id_etudiant) ON DELETE CASCADE,
   FOREIGN KEY(id_enseignement) REFERENCES ENSEIGNEMENT(id_enseignement) ON DELETE CASCADE
);

-- =====================================================
-- DONNÉES DE TEST
-- =====================================================

INSERT INTO FILIERE (Libele_filiere, Nbre_etudiant) VALUES 
('Informatique', 120),
('Gestion', 85),
('Réseaux et Télécommunications', 60),
('Génie Civil', 45),
('Marketing', 70),
('Électronique', 55),
('Biotechnologie', 40);

INSERT INTO MATIERE (Nom_matiere) VALUES 
('Programmation Web'),
('Base de données avancées'),
('Réseaux TCP/IP'),
('Comptabilité générale'),
('Algorithmique'),
('Systèmes d''exploitation'),
('Marketing digital'),
('Résistance des matériaux'),
('Intelligence Artificielle'),
('Cybersécurité'),
('Gestion de projet'),
('Communication professionnelle');

INSERT INTO PERIODE (Date_debut, Date_fin, Libelle_periode) VALUES 
('2025-01-06', '2025-03-28', 'Semestre 2 - 2024/2025'),
('2025-04-07', '2025-06-27', 'Semestre 3 - 2024/2025'),
('2025-09-01', '2025-12-19', 'Semestre 1 - 2025/2026');

INSERT INTO ENSEIGNANT (Nom, Prenom, Mail, Specialite, Diplome, Sexe) VALUES 
('Kouassi', 'Aya', 'aya.kouassi@ecole.ci', 'Développement Web', 'Doctorat en Informatique', 'F'),
('Koné', 'Amadou', 'amadou.kone@ecole.ci', 'Intelligence Artificielle', 'PhD en Machine Learning', 'M'),
('Ouattara', 'Fatoumata', 'fatoumata.ouattara@ecole.ci', 'Cybersécurité', 'Master en Sécurité Informatique', 'F'),
('Bamba', 'Souleymane', 'souleymane.bamba@ecole.ci', 'Réseaux et Télécoms', 'Ingénieur Réseaux Certifié', 'M'),
('Diop', 'Fatou', 'fatou.diop@ecole.sn', 'Comptabilité et Finance', 'Expert-Comptable', 'F'),
('Ndiaye', 'Ousmane', 'ousmane.ndiaye@ecole.sn', 'Marketing Digital', 'MBA en Marketing', 'M'),
('Sall', 'Aminata', 'aminata.sall@ecole.sn', 'Gestion de Projet', 'PMP Certifiée', 'F'),
('Fall', 'Ibrahima', 'ibrahima.fall@ecole.sn', 'Algorithmique', 'Doctorat en Mathématiques', 'M'),
('Tchoumi', 'Esther', 'esther.tchoumi@ecole.cm', 'Biotechnologie', 'PhD en Biologie Moléculaire', 'F'),
('Mboua', 'Jean-Paul', 'jeanpaul.mboua@ecole.cm', 'Génie Civil', 'Ingénieur en Génie Civil', 'M'),
('Ngono', 'Cécile', 'cecile.ngono@ecole.cm', 'Base de données', 'Master en Data Science', 'F'),
('Biya', 'Emmanuel', 'emmanuel.biya@ecole.cm', 'Systèmes d''exploitation', 'Ingénieur Systèmes', 'M'),
('Kaboré', 'Salamata', 'salamata.kabore@ecole.bf', 'Programmation Mobile', 'Master en Développement Mobile', 'F'),
('Ouédraogo', 'Issouf', 'issouf.ouedraogo@ecole.bf', 'Réseaux TCP/IP', 'Ingénieur Réseaux et Sécurité', 'M'),
('Traoré', 'Mariam', 'mariam.traore@ecole.ml', 'Marketing et Communication', 'Master en Communication', 'F'),
('Coulibaly', 'Bakary', 'bakary.coulibaly@ecole.ml', 'Électronique', 'Doctorat en Électronique', 'M'),
('Houngbo', 'Pascaline', 'pascaline.houngbo@ecole.bj', 'Gestion des Ressources Humaines', 'Master en GRH', 'F'),
('Zinsou', 'Théophile', 'theophile.zinsou@ecole.bj', 'Statistiques', 'Doctorat en Statistiques', 'M'),
('Koffi', 'Akossiwa', 'akossiwa.koffi@ecole.tg', 'Droit des affaires', 'Master en Droit', 'F'),
('Améwou', 'Komi', 'komi.amewou@ecole.tg', 'Économie', 'PhD en Économie', 'M');

INSERT INTO ETUDIANT (Nom, Prenom, Sexe, code_filiere) VALUES 
('Koné', 'Issa', 'M', 1),
('Traoré', 'Aïssatou', 'F', 1),
('Ouattara', 'Yacouba', 'M', 1),
('Bamba', 'Naminata', 'F', 1),
('Coulibaly', 'Drissa', 'M', 1),
('Diarrassouba', 'Kadiatou', 'F', 1),
('Touré', 'Seydou', 'M', 2),
('Cissé', 'Mariam', 'F', 2),
('Konaté', 'Lassana', 'M', 2),
('Doumbia', 'Bintou', 'F', 2),
('Sangaré', 'Moussa', 'M', 2),
('Berthé', 'Salimata', 'F', 2),
('Fofana', 'Adama', 'M', 3),
('Diarra', 'Nabintou', 'F', 3),
('Sidibé', 'Brahima', 'M', 3),
('Togola', 'Assetou', 'F', 3),
('Maïga', 'Boubacar', 'M', 3),
('Keita', 'Saran', 'F', 4),
('Bagayoko', 'Siaka', 'M', 4),
('Samaké', 'Oumou', 'F', 4),
('Dembélé', 'Mamadou', 'M', 4),
('Sylla', 'Fanta', 'F', 5),
('Camara', 'Lansana', 'M', 5),
('Kaba', 'Makalé', 'F', 5),
('Condé', 'Sékou', 'M', 5),
('Soro', 'Kigbafory', 'M', 6),
('Goné', 'Sita', 'F', 6),
('Zadi', 'Gnénégbé', 'M', 6),
('Dago', 'Yassongo', 'F', 6),
('Akr', 'Yao', 'M', 7),
('Boni', 'Affoué', 'F', 7),
('Tano', 'Ehouman', 'M', 7),
('Kouamé', 'Amenan', 'F', 7),
('Yéo', 'Losseni', 'M', 1),
('Gbagbo', 'Marie-Josée', 'F', 1),
('Gueï', 'Raoul', 'M', 2),
('Loba', 'Akissi', 'F', 2),
('Tioté', 'Cheick', 'M', 3),
('Boli', 'Micheline', 'F', 3);

INSERT INTO Correspondre (code_filiere, code_matiere, Volume_horaire) VALUES 
(1, 1, 60), (1, 2, 45), (1, 5, 50), (1, 6, 40), (1, 9, 55), (1, 10, 45),
(2, 4, 55), (2, 7, 30), (2, 11, 40), (2, 12, 25),
(3, 3, 70), (3, 6, 35), (3, 10, 50),
(4, 8, 60), (4, 11, 30),
(5, 7, 50), (5, 12, 35), (5, 11, 25),
(6, 5, 45), (6, 6, 40),
(7, 11, 30), (7, 12, 20);