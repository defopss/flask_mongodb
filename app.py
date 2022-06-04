from flask import Flask, render_template, url_for, request, session, redirect, flash
import sys
from flask_pymongo import PyMongo , ObjectId

import bcrypt
from datetime import timedelta
from functools import wraps



app = Flask(__name__)
app.secret_key = "654fg654f(-6599999h'(-èè654œ&é"
#app.config["IMAGE_UPLOADS"] = r"H:\\app\\upload"
app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=59)
mongo = PyMongo(app)



@app.before_request
def make_session_permanent():
    session.permanent = True

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'email' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/admin/login')
  
  return wrap


@app.route('/admin/dash')
@ login_required
def dash():

    return render_template("dash.html")


@app.route('/admin/signup', methods=['POST', 'GET'])
def signup():
    records = mongo.db.user
    message = ''
    if "email" in session:
        return redirect("/admin/dash")
    if request.method == "POST":
        user = request.form.get("name")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        #user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        #if user_found:
            
         #   flash('There already is a user by that name') 
          #  return render_template('signup.html')
        if email_found:
            
            flash('This email already exists in database... Login or create a new account') 
            return render_template('signup.html')
        if password1 != password2:
            
            flash('Passwords should match!') 
            return render_template('signup.html')
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('login.html', email=new_email)
    return render_template('signup.html')
    

@app.route("/admin/login", methods=["POST", "GET"])
def login():
    records = mongo.db.user
    message = 'Please login to your account'
    if "email" in session:
        return redirect("/admin/dash")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect('/admin/dash')
            else:
                if "email" in session:
                    return redirect("/admin/login")
                flash('Wrong password')
                return render_template('login.html')
        else:
            flash('Email not found please signup') 
            return render_template('signup.html')
    return render_template('login.html')

@app.route("/admin/logout", methods=["POST", "GET"])
@ login_required
def logout():
    if "email" in session:
        session.pop("email", None)
        session.clear()
        return render_template("login.html")
    else:
        return render_template('login.html')

@app.route('/admin/insert',  methods=["POST"])
@ login_required
def insert():
    services = mongo.db.liste_services
    if request.method == 'POST':
         services.insert_one(

            {'nom': request.form.get('nom'),
            'oper': request.form.get('oper'),
            'info': request.form.get('info')                       
            })  
    flash('service ajouté avec succées')
    return redirect('/admin/services')


@app.route('/admin/profile')
@ login_required
def profile():

    return render_template("user_profile.html")


@app.route('/admin/services', methods=['POST', 'GET'])
def services():
    services = mongo.db.liste_services
    if request.method == "GET":
        
        data = services.find({})
        print(data)

        return render_template("services.html",data=data)

    return render_template("services.html")
    


# {{ url_for('modifier/{{ service._id }}') }}
@app.route('/admin/modifier', methods=['POST', 'GET'])
@ login_required
def modifier():
    services = mongo.db.liste_services
    
    
    if request.method == 'POST':
        
        
        services.update_one(
            {"_id": ObjectId(request.form.get('id'))},
            {
                "$set": 
                {"nom": request.form.get('nom'),
                "oper": request.form.get('oper'),
                "info": request.form.get('info')
                        }
            })  
    flash('Modification effectue avec seccees')
    return redirect('/admin/services')


@app.route('/admin/supprimer', methods=['POST', 'GET'])
@ login_required
def supprimer():
    services = mongo.db.liste_services
    
    
    if request.method == 'POST':
         services.delete_one({'_id': ObjectId(request.form.get('id'))})

      
    flash('Suppriression effectue avec seccees')
    return redirect('/admin/services')



@app.route('/tt/user/index', methods=['POST', 'GET'])
def index():
    services = mongo.db.liste_services
    if request.method == "GET":
        
        data = services.find({})
        print(data)

        return render_template("index.html",data=data)

    return render_template("index.html")
    






if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5000)