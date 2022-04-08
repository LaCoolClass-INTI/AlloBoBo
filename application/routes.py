from pydoc import doc
from application import app
from flask import render_template, redirect, url_for, request
from application import db
from bson.objectid import ObjectId
from flask_mail import Mail, Message


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/infos_Docteur/<oid>")
def infos_Docteur(oid):
    docteursDB = db.Docteurs
    docteur = docteursDB.find_one({'_id': ObjectId(oid)})
    return render_template("page_docteur.html", docteur = docteur)


@app.route("/annuaire_Docteur")
def annuaire_Docteur():
    docteursDB = db.Docteurs
    docteurs = docteursDB.find({})
    return render_template("Annuaire_DocteursGlobal.html", docteurs = docteurs)


@app.route("/infos_Remede/<oid>")
def infos_Remede(oid):
    RemedeDB = db.Remedes
    remede = RemedeDB.find_one({'_id': ObjectId(oid)})
    return render_template("remede.html", remede = remede)

@app.route("/AnnuaireDocteur", methods={"POST"})
def search_spe():
    speciality = request.form.get('search-doc')
    docteursDB = db.Docteurs
    docteurs = docteursDB.find({'Specialite': speciality})
    return render_template("annuaireDocteur.html", docteurs = docteurs, speciality = speciality)

@app.route("/AnnuaireRemede", methods={"POST"})
def search_remede():
    symptome = request.form.get('search-remede')
    RemedeDB = db.Remedes
    remedes = RemedeDB.find({"Symptome": symptome})
    return render_template("annuaireRemede.html", remedes = remedes, symptome = symptome)


# BETA DU SITE


@app.route('/Contact', methods=['POST', 'GET'])
def contact():
    return render_template('Contact.html')

@app.route('/Qui_sommes_nous', methods=['POST', 'GET'])
def quiNousSommes():
    return render_template('Qui nous sommes.html')

@app.route('/FAQ', methods=['POST', 'GET'])
def faq():
    return render_template('F.A.Q.html')    

@app.route('/Nos_solutions', methods=['POST', 'GET'])
def nosSolutions():
    return render_template('Nos solutions.html')    

@app.route('/Nos offres', methods=['POST', 'GET'])
def nosOffres():
    return render_template('Nos offres.html')

@app.route('/page docteur', methods=['POST', 'GET'])
def docteur():
    return render_template('page docteur.html')

@app.route('/page essential', methods=['POST', 'GET'])
def essential():
    return render_template('page essential.html')

@app.route('/page pharmacy', methods=['POST', 'GET'])
def pharmacy():
    return render_template('page pharmacy.html')  

@app.route('/RGPD', methods=['POST', 'GET'])
def RGPD():
    return render_template('RGPD.html')  

@app.route('/Connexion', methods=['POST', 'GET'])
def connexion():
    return render_template('connexion.html')  

@app.route('/Inscription', methods=['POST', 'GET'])
def inscription():
    return render_template('inscription.html')  

@app.route('/A_propos_de_AlloBobo', methods=['POST', 'GET'])
def apropos():
    return render_template('À propos de AlloBobo.html') 

@app.route('/professionnels_de_sante', methods=['POST', 'GET'])
def pro():
    return render_template('professionnels_de_sante.html') 

@app.route('/Condition_utilisation', methods=['POST', 'GET'])
def cdtgeneral():
    return render_template('CGU.html') 

@app.route('/send')
def send():

    msg = Message('sujet', 
                sender = request.form.get('email'),
                recipients=['lacoolclass@gmail.com'])
    msg.body = 'message'
    msg.html = 'nom "<br/>" addmail "<br/>" msag'

    Mail.send = (msg)
    return render_template('Contact.html')