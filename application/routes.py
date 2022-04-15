from pydoc import doc
from application import app
from flask import render_template, redirect, url_for, request, session
from application import db
from bson.objectid import ObjectId
import pymongo
import bcrypt
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'lacoolclass@gmail.com'
app.config['MAIL_PASSWORD'] = 'intijee-16'

mail = Mail(app)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("connexion.html")
    else:
        return render_template('index.html')

@app.route("/index")
def index():
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        return render_template("index.html", user = user)
    else:
        return render_template("connexion.html")

@app.route("/Redirection/<page>")
def redirection(page):
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        return render_template(page, user = user)
    elif page=="RGPD.html":
        return render_template(page)
    elif page=="À propos de AlloBobo.html":
        return render_template(page)
    elif page=="CGU.html":
        return render_template(page)
    elif page=="professionnels_de_sante.html":
        return render_template(page)
    else:
        return render_template('connexion.html')

@app.route("/Mot-de-passe-oublié")
def mdp_oublie():
    return render_template("MDP_oublie.html")    

@app.route("/", methods=["POST", "GET"])
def connexion():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        email_found = db.session.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('index'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('connexion.html', message=message)
        else:
            message = 'Email not found'
            return render_template('connexion.html', message=message)
    return render_template('connexion.html', message=message)    

@app.route("/Inscription", methods=['POST', 'GET'])
def inscription():
    message = ''
    if "email" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        user = request.form.get("pseudo")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        dbSession = db.session
        user_found = dbSession.find_one({"pseudo": user})
        email_found = dbSession.find_one({"email": email})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('inscription.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('inscription.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('inscription.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'pseudo': user, 'email': email, 'password': hashed}
            dbSession.insert_one(user_input)
            
            user_data = dbSession.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('index.html', email=new_email)
    return render_template('inscription.html')   

@app.route("/infos_Docteur/<oid>")
def infos_Docteur(oid):
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        docteursDB = db.Docteurs
        docteur = docteursDB.find_one({'_id': ObjectId(oid)})
        return render_template("page_docteur.html", docteur = docteur, user=user)
    else:
        return render_template("connexion.html")


@app.route("/annuaire_Docteur")
def annuaire_Docteur():
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        docteursDB = db.Docteurs
        docteurs = docteursDB.find({})
        return render_template("Annuaire_DocteursGlobal.html", docteurs = docteurs, user=user)
    else:
       return render_template("connexion.html") 


@app.route("/infos_Remede/<oid>")
def infos_Remede(oid):
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        RemedeDB = db.Remedes
        remede = RemedeDB.find_one({'_id': ObjectId(oid)})
        return render_template("remede.html", remede = remede, user=user)
    else:
       return render_template("connexion.html") 

@app.route("/AnnuaireDocteur", methods={"POST"})
def search_spe():
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        speciality = request.form.get('search-doc')
        docteursDB = db.Docteurs
        docteurs = docteursDB.find({'Specialite': speciality})
        return render_template("annuaireDocteur.html", docteurs = docteurs, speciality = speciality, user=user)
    else:
       return render_template("connexion.html")

@app.route("/AnnuaireRemede", methods={"POST"})
def search_remede():
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        symptome = request.form.get('search-remede')
        RemedeDB = db.Remedes
        remedes = RemedeDB.find({"Symptome": symptome})
        return render_template("annuaireRemede.html", remedes = remedes, symptome = symptome, user=user)
    else:
       return render_template("connexion.html")

@app.route('/Nos offres', methods=['POST', 'GET'])
def nosOffres():
    if 'email' in session:
        email = session['email']
        user = db.session.find_one({'email': email})
        RemedeDB = db.Remedes
        remedes = RemedeDB.find({})
        return render_template("Nos offres.html", remedes = remedes, user=user)
    else:
       return render_template("connexion.html")




# BETA DU SITE


@app.route('/Contact', methods=['POST', 'GET'])
def contact():
    page = "Contact.html"
    return redirect(url_for('redirection', page=page))

@app.route('/Qui_sommes_nous', methods=['POST', 'GET'])
def quiNousSommes():
    page = "Qui nous sommes.html"
    return redirect(url_for('redirection', page=page))

@app.route('/FAQ', methods=['POST', 'GET'])
def faq():
    page = "F.A.Q.html"
    return redirect(url_for('redirection', page=page))

@app.route('/Nos_solutions', methods=['POST', 'GET'])
def nosSolutions():
    page = "Nos solutions.html"
    return redirect(url_for('redirection', page=page)) 

@app.route('/page docteur', methods=['POST', 'GET'])
def docteur():
    page = "page docteur.html"
    return redirect(url_for('redirection', page=page))


@app.route('/RGPD', methods=['POST', 'GET'])
def RGPD():
    page = "RGPD.html"
    return redirect(url_for('redirection', page=page))  

@app.route('/Connexion', methods=['POST', 'GET'])
def connexion2():
    return render_template('connexion.html')  

@app.route('/A_propos_de_AlloBobo', methods=['POST', 'GET'])
def apropos():
    page = "À propos de AlloBobo.html"
    return redirect(url_for('redirection', page=page))  

@app.route('/professionnels_de_sante', methods=['POST', 'GET'])
def pro():
    page = "professionnels_de_sante.html"
    return redirect(url_for('redirection', page=page))

@app.route('/Condition_utilisation', methods=['POST', 'GET'])
def cdtgeneral():
    page = "CGU.html"
    return redirect(url_for('redirection', page=page))

@app.route('/page bigdata', methods=['POST', 'GET'])
def bigdata():
    page = "page_BigData.html"
    return redirect(url_for('redirection', page=page))
@app.route('/send', methods=['POST', 'GET'])
def send():
    msg = Message('Sujet 1',
        sender = 'mec.cheloudufinfonddelariege@gmail.com',
        recipients=['lacoolclass@gmail.com'])
    mail.send(msg)

    return 'Message envoyé'