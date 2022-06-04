from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo , ObjectId
import bcrypt
import os
from os import urandom
from datetime import timedelta
from pprint import pprint
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 

application = Flask(__name__)
application.secret_key = "654fg654f(-654h'(-èè654œ&é"
#app.config["IMAGE_UPLOADS"] = r"H:\\application\\upload"
application.config['MONGO_DBNAME'] = 'unictdb'
application.config['MONGO_URI'] = 'mongodb://localhost:27017/unictdb'
application.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=59)
mongo = PyMongo(application)

@application.before_request
def make_session_permanent():
    session.permanent = True


#######################################################################################################################################
"""

@application.route('/editrech/<id>', methods=['POST', 'GET'])
def edit_rech(id):
    listrech = mongo.db.e2_personne_en_rech
    item = listrech.find_one({'_id': ObjectId(id)})

    if request.method == 'GET':
     if session['username'] is not None:
        print(item)
        return render_template('editrech.html', username=session['username'], item=item)




    mongo.db.e2_personne_en_rech.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": 
            {"cin": request.form.get('cin'),
            "doc": request.form.get('doc'),
            "date": request.form.get('date')
                    }
        })  
    flash('تم تعديل المعطيات بنجاح')
    return redirect(url_for('searchrec'))


@application.route('/editm/<id>', methods=['POST', 'GET'])
def edit_m(id):
    listarr = mongo.db.e3_personne_en_arr
    item_m = listarr.find_one({'_id': ObjectId(id)})

    if request.method == 'GET':
     if session['username'] is not None:
        print(item_m)
        return render_template('editm.html', username=session['username'], item=item_m)



    mongo.db.e3_personne_en_arr.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": 
            {"cin": request.form.get('cin'),
            "doc": request.form.get('doc'),
            "date": request.form.get('date')
                    }
        })  
    flash('تم تعديل المعطيات بنجاح')
    return redirect(url_for('searchm'))

@application.route('/editoptech/<id>', methods=['POST', 'GET'])
def edit_optech(id):
    listper = mongo.db.list_personnes
    item_per = listper.find_one({'_id': ObjectId(id)})

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('editoptech.html', username=session['username'], item=item_per)



    mongo.db.list_personnes.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": 
            {'الولاية': request.form.get('gov'),
            'الهوية': request.form.get('cin'),
            "doc": request.form.get('doc')
                    }
        })  
    flash('تم تعديل المعطيات بنجاح')
    return redirect(url_for('searchoptech'))

#--------------------------
@application.route('/addrech', methods=['POST', 'GET'])
def addrech():

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('addform.html', username=session['username'])




    mongo.db.e2_personne_en_rech.insert(
        
        
            {'cin': request.form.get('cin'),
            'doc': request.form.get('doc'),
            'date': request.form.get('date')
                    
        })  
    flash('تم اضــافة المعطيات بنجاح')
    return redirect(url_for('searchrec'))

@application.route('/addm', methods=['POST', 'GET'])
def addm():

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('addformm.html', username=session['username'])



    mongo.db.e3_personne_en_arr.insert(
        
        
            {'cin': request.form.get('cin'),
            'doc': request.form.get('doc'),
            'date': request.form.get('date')
                    
        })  
    flash('تم اضــافة المعطيات بنجاح')
    return redirect(url_for('searchm'))

@application.route('/addoptech', methods=['POST', 'GET'])
def addoptech():

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('addformoptech.html', username=session['username'])



    mongo.db.list_personnes.insert(
        
        
            {'الولاية': request.form.get('gov'),
            'الهوية': request.form.get('cin'),
            "doc": request.form.get('doc')
                    
                    
        })  
    flash('تم اضــافة المعطيات بنجاح')
    return redirect(url_for('searchoptech'))




#-----------------------------------

@application.route('/reg', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.usersdata
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            #return redirect(url_for('login'))
            return render_template('login.html')
        
        return 'That username already exists!'

    return render_template('reg.html')

"""
#######################################################################################################################################

@application.route("/")
def index():
    if 'username' in session:
        
        return redirect(url_for('gohome'))

    return render_template('login.html')

@application.route("/home")
def gohome():
    if 'username' in session:
        message= session['username']

        return render_template("index.html", message=message)
    return render_template('login.html')




@application.route('/login', methods=['POST'])
def login():
    
        users = mongo.db.usersdata
        login_user = users.find_one({'username' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                
                return redirect(url_for('index'))

        return 'Invalid username/password combination'


@application.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.clear()
   return redirect(url_for('index'))


@application.route("/searchrec", methods=['POST', 'GET'])
def searchrec():
    if 'username' in session:
        if request.method == "POST":
            text = request.form['text']
            listpersonnes = mongo.db.e2_personne_en_rech
            data = listpersonnes.find( { 'cin' :  {'$regex': text} } )
            return render_template('/user/searchrec.html', data=data)
        return render_template('/user/searchrec.html')
    return render_template('login.html')

@application.route("/searchm", methods=['POST', 'GET'])
def searchm():
    if 'username' in session:
        if request.method == "POST":
            text = request.form['text']
            listpersonnes = mongo.db.e3_personne_en_arr
            data = listpersonnes.find( { 'cin' :  {'$regex': text} } )
            return render_template('/user/searchm.html', data=data)
        return render_template('/user/searchm.html')
    return render_template('login.html')


@application.route("/searchoptech", methods=['POST', 'GET'])
def searchoptech():
    if 'username' in session:
        if request.method == "POST":
            text = request.form['text']
            listpersonnes = mongo.db.list_personnes
            data = listpersonnes.find( { 'الهوية' :  {'$regex': text} } )
            return render_template('/user/searchoptech.html', data=data)
        return render_template('/user/searchoptech.html')
    return render_template('login.html')
      



if __name__ == "__main__":
    application.debug = True
    application.run(debug=True,port=8003)

    
