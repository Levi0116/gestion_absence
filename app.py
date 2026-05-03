# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models.database import RapportModel
from config import Config
import os
from models.database import (
    PeriodeModel, MatiereModel, EnseignantModel, 
    FiliereModel, CorrespondreModel, Database,
    EtudiantModel, EnseignementModel, AssisterModel, MessageModel
)

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation lazy des modèles (à la demande)
def get_models():
    return {
        'periode': PeriodeModel(),
        'matiere': MatiereModel(),
        'enseignant': EnseignantModel(),
        'filiere': FiliereModel(),
        'correspondre': CorrespondreModel(),
        'etudiant': EtudiantModel(),
        'enseignement': EnseignementModel(),
        'assister': AssisterModel(),
        'message': MessageModel(),
        'rapport': RapportModel()
    }

# ============= ROUTES PRINCIPALES =============
@app.route('/')
def index():
    # Récupérer les compteurs pour le tableau de bord
    nb_periodes = len(periode_model.get_all() or [])
    nb_matieres = len(matiere_model.get_all() or [])
    nb_enseignants = len(enseignant_model.get_all() or [])
    nb_filieres = len(filiere_model.get_all() or [])
    nb_etudiants = etudiant_model.count_all()
    nb_enseignements = enseignement_model.count_all()
    nb_absences = assister_model.count_absences_non_justifiees()
    
    return render_template('index.html',
                         nb_periodes=nb_periodes,
                         nb_matieres=nb_matieres,
                         nb_enseignants=nb_enseignants,
                         nb_filieres=nb_filieres,
                         nb_etudiants=nb_etudiants,
                         nb_enseignements=nb_enseignements,
                         nb_absences=nb_absences)

# ============= ROUTES PÉRIODES (existantes) =============
@app.route('/periodes')
def periodes_index():
    periodes = periode_model.get_all()
    return render_template('periode/index.html', periodes=periodes)

@app.route('/periodes/ajouter', methods=['GET', 'POST'])
def periode_ajouter():
    if request.method == 'POST':
        libelle = request.form['libelle']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        periode_model.create(libelle, date_debut, date_fin)
        flash('Période ajoutée avec succès', 'success')
        return redirect(url_for('periodes_index'))
    return render_template('periode/ajouter.html')

@app.route('/periodes/modifier/<int:id>', methods=['GET', 'POST'])
def periode_modifier(id):
    periode = periode_model.get_by_id(id)
    if not periode:
        flash('Période non trouvée', 'error')
        return redirect(url_for('periodes_index'))
    
    if request.method == 'POST':
        libelle = request.form['libelle']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        periode_model.update(id, libelle, date_debut, date_fin)
        flash('Période modifiée avec succès', 'success')
        return redirect(url_for('periodes_index'))
    
    return render_template('periode/modifier.html', periode=periode)

@app.route('/periodes/supprimer/<int:id>')
def periode_supprimer(id):
    periode_model.delete(id)
    flash('Période supprimée avec succès', 'success')
    return redirect(url_for('periodes_index'))

# ============= ROUTES MATIÈRES (existantes) =============
@app.route('/matieres')
def matieres_index():
    matieres = matiere_model.get_all()
    return render_template('matiere/index.html', matieres=matieres)

@app.route('/matieres/ajouter', methods=['GET', 'POST'])
def matiere_ajouter():
    if request.method == 'POST':
        nom = request.form['nom_matiere']
        matiere_model.create(nom)
        flash('Matière ajoutée avec succès', 'success')
        return redirect(url_for('matieres_index'))
    return render_template('matiere/ajouter.html')

@app.route('/matieres/modifier/<int:id>', methods=['GET', 'POST'])
def matiere_modifier(id):
    matiere = matiere_model.get_by_id(id)
    if not matiere:
        flash('Matière non trouvée', 'error')
        return redirect(url_for('matieres_index'))
    
    if request.method == 'POST':
        nom = request.form['nom_matiere']
        matiere_model.update(id, nom)
        flash('Matière modifiée avec succès', 'success')
        return redirect(url_for('matieres_index'))
    
    return render_template('matiere/modifier.html', matiere=matiere)

@app.route('/matieres/supprimer/<int:id>')
def matiere_supprimer(id):
    matiere_model.delete(id)
    flash('Matière supprimée avec succès', 'success')
    return redirect(url_for('matieres_index'))

# ============= ROUTES ENSEIGNANTS (existantes) =============
@app.route('/enseignants')
def enseignants_index():
    enseignants = enseignant_model.get_all()
    return render_template('enseignant/index.html', enseignants=enseignants)

@app.route('/enseignants/ajouter', methods=['GET', 'POST'])
def enseignant_ajouter():
    if request.method == 'POST':
        enseignant_model.create(
            request.form['nom'],
            request.form['prenom'],
            request.form['mail'],
            request.form['specialite'],
            request.form['diplome'],
            request.form['sexe']
        )
        flash('Enseignant ajouté avec succès', 'success')
        return redirect(url_for('enseignants_index'))
    return render_template('enseignant/ajouter.html')

@app.route('/enseignants/modifier/<int:id>', methods=['GET', 'POST'])
def enseignant_modifier(id):
    enseignant = enseignant_model.get_by_id(id)
    if not enseignant:
        flash('Enseignant non trouvé', 'error')
        return redirect(url_for('enseignants_index'))
    
    if request.method == 'POST':
        enseignant_model.update(
            id,
            request.form['nom'],
            request.form['prenom'],
            request.form['mail'],
            request.form['specialite'],
            request.form['diplome'],
            request.form['sexe']
        )
        flash('Enseignant modifié avec succès', 'success')
        return redirect(url_for('enseignants_index'))
    
    return render_template('enseignant/modifier.html', enseignant=enseignant)

@app.route('/enseignants/supprimer/<int:id>')
def enseignant_supprimer(id):
    enseignant_model.delete(id)
    flash('Enseignant supprimé avec succès', 'success')
    return redirect(url_for('enseignants_index'))

# ============= ROUTES FILIÈRES (existantes) =============
@app.route('/filieres')
def filieres_index():
    filieres = filiere_model.get_all()
    return render_template('filiere/index.html', filieres=filieres)

@app.route('/filieres/ajouter', methods=['GET', 'POST'])
def filiere_ajouter():
    if request.method == 'POST':
        filiere_model.create(
            request.form['libelle'],
            request.form['nbre_etudiant'] or 0
        )
        flash('Filière ajoutée avec succès', 'success')
        return redirect(url_for('filieres_index'))
    return render_template('filiere/ajouter.html')

@app.route('/filieres/modifier/<int:id>', methods=['GET', 'POST'])
def filiere_modifier(id):
    filiere = filiere_model.get_by_id(id)
    if not filiere:
        flash('Filière non trouvée', 'error')
        return redirect(url_for('filieres_index'))
    
    if request.method == 'POST':
        filiere_model.update(
            id,
            request.form['libelle'],
            request.form['nbre_etudiant']
        )
        flash('Filière modifiée avec succès', 'success')
        return redirect(url_for('filieres_index'))
    
    return render_template('filiere/modifier.html', filiere=filiere)

@app.route('/filieres/supprimer/<int:id>')
def filiere_supprimer(id):
    filiere_model.delete(id)
    flash('Filière supprimée avec succès', 'success')
    return redirect(url_for('filieres_index'))

# ============= ROUTES ASSOCIATIONS (existantes) =============
@app.route('/correspondre')
def correspondre_index():
    associations = correspondre_model.get_all_with_names()
    filieres = filiere_model.get_all()
    matieres = matiere_model.get_all()
    return render_template('correspondre/index.html', 
                         associations=associations,
                         filieres=filieres,
                         matieres=matieres)

@app.route('/correspondre/ajouter', methods=['POST'])
def correspondre_ajouter():
    try:
        correspondre_model.create(
            request.form['code_filiere'],
            request.form['code_matiere'],
            request.form['volume_horaire']
        )
        flash('Association créée avec succès', 'success')
    except Exception as e:
        flash('Cette association existe déjà ou une erreur est survenue', 'error')
    return redirect(url_for('correspondre_index'))

@app.route('/correspondre/supprimer/<int:filiere>/<int:matiere>')
def correspondre_supprimer(filiere, matiere):
    correspondre_model.delete(filiere, matiere)
    flash('Association supprimée avec succès', 'success')
    return redirect(url_for('correspondre_index'))

# ============= NOUVELLES ROUTES - ÉTUDIANTS =============
@app.route('/etudiants')
def etudiants_index():
    etudiants = etudiant_model.get_all()
    filieres = filiere_model.get_all()
    return render_template('etudiant/index.html', etudiants=etudiants, filieres=filieres)

@app.route('/etudiants/ajouter', methods=['GET', 'POST'])
def etudiant_ajouter():
    if request.method == 'POST':
        etudiant_model.create(
            request.form['nom'],
            request.form['prenom'],
            request.form['sexe'],
            request.form['code_filiere']
        )
        flash('Étudiant ajouté avec succès', 'success')
        return redirect(url_for('etudiants_index'))
    
    filieres = filiere_model.get_all()
    return render_template('etudiant/ajouter.html', filieres=filieres)

@app.route('/etudiants/modifier/<int:id>', methods=['GET', 'POST'])
def etudiant_modifier(id):
    etudiant = etudiant_model.get_by_id(id)
    if not etudiant:
        flash('Étudiant non trouvé', 'error')
        return redirect(url_for('etudiants_index'))
    
    if request.method == 'POST':
        etudiant_model.update(
            id,
            request.form['nom'],
            request.form['prenom'],
            request.form['sexe'],
            request.form['code_filiere']
        )
        flash('Étudiant modifié avec succès', 'success')
        return redirect(url_for('etudiants_index'))
    
    filieres = filiere_model.get_all()
    return render_template('etudiant/modifier.html', etudiant=etudiant, filieres=filieres)

@app.route('/etudiants/supprimer/<int:id>')
def etudiant_supprimer(id):
    etudiant_model.delete(id)
    flash('Étudiant supprimé avec succès', 'success')
    return redirect(url_for('etudiants_index'))

@app.route('/etudiants/<int:id>/absences')
def etudiant_absences(id):
    etudiant = etudiant_model.get_by_id(id)
    if not etudiant:
        flash('Étudiant non trouvé', 'error')
        return redirect(url_for('etudiants_index'))
    
    absences = assister_model.get_absences_by_etudiant(id)
    stats = etudiant_model.get_absences_stats(id)
    
    return render_template('etudiant/absences.html',
                         etudiant=etudiant, absences=absences, stats=stats)

# ============= NOUVELLES ROUTES - ENSEIGNEMENTS =============
@app.route('/enseignements')
def enseignements_index():
    enseignements = enseignement_model.get_all()
    return render_template('enseignement/index.html', enseignements=enseignements)

@app.route('/enseignements/ajouter', methods=['GET', 'POST'])
def enseignement_ajouter():
    if request.method == 'POST':
        enseignement_model.create(
            request.form['date_enseignement'],
            request.form['horaire_debut'],
            request.form['horaire_fin'],
            request.form['id_enseignant'],
            request.form['code_filiere'],
            request.form['id_periode'],
            request.form['code_matiere']
        )
        flash('Séance programmée avec succès', 'success')
        return redirect(url_for('enseignements_index'))
    
    enseignants = enseignant_model.get_all()
    filieres = filiere_model.get_all()
    periodes = periode_model.get_all()
    matieres = matiere_model.get_all()
    
    return render_template('enseignement/ajouter.html',
                         enseignants=enseignants, filieres=filieres,
                         periodes=periodes, matieres=matieres)

@app.route('/enseignements/<int:id>/fiche')
def enseignement_fiche(id):
    enseignement = enseignement_model.get_by_id(id)
    if not enseignement:
        flash('Séance non trouvée', 'error')
        return redirect(url_for('enseignements_index'))
    
    etudiants = enseignement_model.get_presences(id)
    
    return render_template('enseignement/fiche.html',
                         enseignement=enseignement, etudiants=etudiants)

@app.route('/enseignements/<int:id>/saisie', methods=['GET', 'POST'])
def absence_saisie(id):
    enseignement = enseignement_model.get_by_id(id)
    if not enseignement:
        flash('Séance non trouvée', 'error')
        return redirect(url_for('enseignements_index'))
    
    if request.method == 'POST':
        presences = {}
        for key, value in request.form.items():
            if key.startswith('presence_'):
                id_etudiant = key.replace('presence_', '')
                presences[id_etudiant] = value
        
        if assister_model.save_presences(id, presences):
            flash('Présences enregistrées avec succès', 'success')
        else:
            flash('Erreur lors de l\'enregistrement', 'error')
        
        return redirect(url_for('enseignement_fiche', id=id))
    
    etudiants = enseignement_model.get_presences(id)
    return render_template('absence/saisie.html',
                         enseignement=enseignement, etudiants=etudiants)

@app.route('/enseignements/supprimer/<int:id>')
def enseignement_supprimer(id):
    enseignement_model.delete(id)
    flash('Séance supprimée avec succès', 'success')
    return redirect(url_for('enseignements_index'))

# ============= NOUVELLES ROUTES - ABSENCES =============
@app.route('/absences')
def absences_index():
    filiere = request.args.get('filiere', type=int)
    absences = assister_model.get_absences_non_justifiees(code_filiere=filiere)
    filieres = filiere_model.get_all()
    return render_template('absence/index.html',
                         absences=absences, filieres=filieres, selected_filiere=filiere)

@app.route('/absence/justifier/<int:etudiant>/<int:enseignement>', methods=['GET', 'POST'])
def absence_justifier(etudiant, enseignement):
    if request.method == 'POST':
        motif = request.form['motif']
        assister_model.justifier_absence(etudiant, enseignement, motif)
        flash('Absence justifiée avec succès', 'success')
        return redirect(url_for('absences_index'))
    
    etudiant_info = etudiant_model.get_by_id(etudiant)
    enseignement_info = enseignement_model.get_by_id(enseignement)
    
    return render_template('absence/justifier.html',
                         etudiant=etudiant_info, enseignement=enseignement_info)

# ============= NOUVELLES ROUTES - MESSAGES =============
@app.route('/message/<int:etudiant>')
def generer_message(etudiant):
    absences = assister_model.get_absences_by_etudiant(etudiant)
    message = message_model.generer_message_absence(etudiant, absences)
    etudiant_info = etudiant_model.get_by_id(etudiant)
    
    return render_template('message/notification.html',
                         etudiant=etudiant_info, message=message, absences=absences)

# ============= ROUTES STATISTIQUES =============
@app.route('/statistiques')
def statistiques_index():
    stats = assister_model.get_statistiques_globales()
    return render_template('statistiques/index.html', stats=stats)

# ============= API JSON =============
@app.route('/api/matieres-par-filiere/<int:filiere>')
def api_matieres_par_filiere(filiere):
    db = Database()
    query = """
        SELECT m.code_matiere, m.Nom_matiere 
        FROM MATIERE m
        JOIN Correspondre c ON m.code_matiere = c.code_matiere
        WHERE c.code_filiere = %s
        ORDER BY m.Nom_matiere
    """
    result = db.execute_query(query, (filiere,), fetch=True)
    return jsonify(result if result else [])

@app.route('/api/etudiants-par-filiere/<int:filiere>')
def api_etudiants_par_filiere(filiere):
    etudiants = etudiant_model.get_by_filiere(filiere)
    return jsonify(etudiants if etudiants else [])

# ============= DÉMARRAGE =============
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
# ============= MODULE 3 - ROUTES D'ÉDITION/CONSULTATION =============

@app.route('/module3')
def module3_index():
    """Accueil du module 3 - Édition"""
    stats = rapport_model.get_statistiques_avancees()
    return render_template('module3/index.html', stats=stats)

# ============= MATIÈRES PAR FILIÈRE =============
@app.route('/module3/matieres-par-filiere')
def module3_matieres_par_filiere():
    code_filiere = request.args.get('filiere', type=int)
    matieres = rapport_model.get_matieres_par_filiere(code_filiere)
    filieres = filiere_model.get_all()
    
    # Regrouper par filière
    filieres_dict = {}
    for matiere in matieres:
        key = matiere['code_filiere']
        if key not in filieres_dict:
            filieres_dict[key] = {
                'filiere': matiere['Libele_filiere'],
                'nbre_etudiant': matiere['Nbre_etudiant'],
                'matieres': []
            }
        filieres_dict[key]['matieres'].append(matiere)
    
    return render_template('module3/matieres_par_filiere.html',
                         filieres_dict=filieres_dict,
                         filieres=filieres,
                         selected_filiere=code_filiere)

# ============= ABSENCES PAR FILIÈRE ET PÉRIODE =============
@app.route('/module3/absences-par-filiere-periode')
def module3_absences_par_filiere_periode():
    code_filiere = request.args.get('filiere', type=int)
    id_periode = request.args.get('periode', type=int)
    
    absences = rapport_model.get_absences_par_filiere_periode(code_filiere, id_periode)
    filieres = filiere_model.get_all()
    periodes = periode_model.get_all()
    
    return render_template('module3/absences_filiere_periode.html',
                         absences=absences,
                         filieres=filieres,
                         periodes=periodes,
                         selected_filiere=code_filiere,
                         selected_periode=id_periode)

# ============= ABSENCES PAR ÉTUDIANT =============
@app.route('/module3/absences-par-etudiant')
def module3_absences_par_etudiant():
    code_filiere = request.args.get('filiere', type=int)
    id_periode = request.args.get('periode', type=int)
    search = request.args.get('search', '').strip()
    
    etudiants = rapport_model.get_absences_par_etudiant(
        code_filiere=code_filiere,
        id_periode=id_periode
    )
    
    # Filtrer par recherche si nécessaire
    if search:
        etudiants = [e for e in etudiants if 
                     search.lower() in e['Nom'].lower() or 
                     search.lower() in e['Prenom'].lower()]
    
    filieres = filiere_model.get_all()
    periodes = periode_model.get_all()
    
    return render_template('module3/absences_par_etudiant.html',
                         etudiants=etudiants,
                         filieres=filieres,
                         periodes=periodes,
                         selected_filiere=code_filiere,
                         selected_periode=id_periode,
                         search=search)

# ============= DÉTAIL ÉTUDIANT =============
@app.route('/module3/etudiant/<int:id>/detail')
def module3_etudiant_detail(id):
    etudiant = etudiant_model.get_by_id(id)
    if not etudiant:
        flash('Étudiant non trouvé', 'error')
        return redirect(url_for('module3_absences_par_etudiant'))
    
    details = rapport_model.get_detail_etudiant(id)
    resume = rapport_model.get_resume_etudiant(id)
    
    return render_template('module3/etudiant_detail.html',
                         etudiant=etudiant,
                         details=details,
                         resume=resume)

# ============= LISTE DES ABSENCES JUSTIFIÉES =============

@app.route('/module3/absences-justifiees')
def module3_absences_justifiees():
    code_filiere = request.args.get('filiere', type=int)
    id_periode = request.args.get('periode', type=int)
    
    # CORRECTION : S'assurer que justifiees est une liste
    justifiees = rapport_model.get_absences_justifiees(code_filiere, id_periode)
    if justifiees is None:
        justifiees = []
    
    filieres = filiere_model.get_all()
    periodes = periode_model.get_all()
    
    return render_template('module3/absences_justifiees.html',
                         justifiees=justifiees,
                         filieres=filieres,
                         periodes=periodes,
                         selected_filiere=code_filiere,
                         selected_periode=id_periode)
    
# ============= EXPORT CSV =============
@app.route('/module3/export/absences-par-etudiant')
def module3_export_absences_etudiant():
    """Export CSV des absences par étudiant"""
    import csv
    from io import StringIO
    from flask import Response
    
    code_filiere = request.args.get('filiere', type=int)
    id_periode = request.args.get('periode', type=int)
    
    etudiants = rapport_model.get_absences_par_etudiant(code_filiere, id_periode)
    
    si = StringIO()
    cw = csv.writer(si, delimiter=';')
    cw.writerow(['ID', 'Nom', 'Prénom', 'Sexe', 'Filière', 'Total Séances', 
                 'Présences', 'Absences', 'Justifiées', 'Pénalité', 'Taux Présence'])
    
    for e in etudiants:
        cw.writerow([
            e['id_etudiant'], e['Nom'], e['Prenom'], e['Sexe'],
            e['Libele_filiere'], e['total_seances'] or 0,
            e['nb_presences'] or 0, e['nb_absences'] or 0,
            e['nb_justifiees'] or 0, e['penalite'] or 0,
            f"{e['taux_presence'] or 0}%"
        ])
    
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=absences_par_etudiant.csv"}
    )

@app.route('/module3/export/absences-justifiees')
def module3_export_absences_justifiees():
    """Export CSV des absences justifiées"""
    import csv
    from io import StringIO
    from flask import Response
    
    code_filiere = request.args.get('filiere', type=int)
    id_periode = request.args.get('periode', type=int)
    
    justifiees = rapport_model.get_absences_justifiees(code_filiere, id_periode)
    
    si = StringIO()
    cw = csv.writer(si, delimiter=';')
    cw.writerow(['Étudiant', 'Filière', 'Date', 'Matière', 'Motif', 
                 'Date Justification', 'Enseignant', 'Période'])
    
    for j in justifiees:
        cw.writerow([
            f"{j['Prenom']} {j['Nom']}", j['Libele_filiere'],
            j['Date_enseignement'], j['Nom_matiere'],
            j['motif_justification'] or '', j['date_justification'] or '',
            f"{j['prenom_enseignant']} {j['nom_enseignant']}",
            j['Libelle_periode']
        ])
    
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=absences_justifiees.csv"}
    )