# test_connexion.py
import mysql.connector

# Configuration (identique à votre .env)
config = {
    'host': 'localhost',
    'user': 'Levi',
    'password': 'KfjL01162004',
    'database': 'gestion_absences',
    'port': 3306
}

print("=" * 50)
print("TEST DE CONNEXION ET RÉCUPÉRATION DES DONNÉES")
print("=" * 50)

try:
    # Connexion
    conn = mysql.connector.connect(**config)
    print("✅ Connexion réussie !")
    
    cursor = conn.cursor(dictionary=True)
    
    # Test FILIERE
    cursor.execute("SELECT * FROM FILIERE")
    filieres = cursor.fetchall()
    print(f"\n📊 FILIERE : {len(filieres)} enregistrements")
    for f in filieres:
        print(f"   - {f['code_filiere']} : {f['Libele_filiere']} ({f['Nbre_etudiant']} étudiants)")
    
    # Test MATIERE
    cursor.execute("SELECT * FROM MATIERE")
    matieres = cursor.fetchall()
    print(f"\n📊 MATIERE : {len(matieres)} enregistrements")
    for m in matieres[:3]:
        print(f"   - {m['code_matiere']} : {m['Nom_matiere']}")
    
    # Test PERIODE
    cursor.execute("SELECT * FROM PERIODE")
    periodes = cursor.fetchall()
    print(f"\n📊 PERIODE : {len(periodes)} enregistrements")
    for p in periodes:
        print(f"   - {p['id_periode']} : {p['Libelle_periode']}")
    
    # Test ENSEIGNANT
    cursor.execute("SELECT * FROM ENSEIGNANT")
    enseignants = cursor.fetchall()
    print(f"\n📊 ENSEIGNANT : {len(enseignants)} enregistrements")
    for e in enseignants[:3]:
        print(f"   - {e['id_enseignant']} : {e['Prenom']} {e['Nom']}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur : {e}")

print("\n" + "=" * 50)