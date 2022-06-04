from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo , ObjectId
import bcrypt
import folium
import shutil
import os.path
import os,io,sys,io
from os import urandom , path
from datetime import timedelta
from pprint import pprint
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 
import subprocess,platform
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
            listpersonnes = mongo.db.list                             # 2 s
            data = listpersonnes.find( { 'cin' :  {'$regex': text} } )        # cin
            return render_template('/optech/searchoptech.html', data=data)
        return render_template('/optech/searchoptech.html')
    return render_template('login.html')

@application.route('/addoptech', methods=['POST', 'GET'])
def addoptech():

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('/optech/addformoptechc.html', username=session['username'])


    image = request.files["image"]
    cinn = request.form.get('cinn')
    mongo.db.list.insert(
        
        
            {'gov': request.form.get('gov'),
            'cin': request.form.get('cin'),
            'cinn': request.form.get('cinn'),
            "doc": request.form.get('doc'),
            "mobiles": request.form.get('mobiles'),
            "rxfb": request.form.get('rxfb'),
            "rxtlg": request.form.get('rxtlg'),
            "rxwa": request.form.get('rxwa'),
            "appareil": request.form.get('appareil'),
            "autres": request.form.get('autres'),
            "sd": request.form.get('sd')            
        })  
    print(cinn)
    folder = os.path.join("/home/devops/Bureau/unict_app/codzz/app/static/uploads",cinn)
    #print(folder)
    os.makedirs(folder) 
    image.save(os.path.join(folder,(cinn+".jpg")))
    
    flash('تم اضــافة المعطيات بنجاح')
    return redirect(url_for('searchoptech'))

@application.route('/editoptech/<id>', methods=['POST', 'GET'])
def editoptech(id):
    listper = mongo.db.list
    item_per = listper.find_one({'_id': ObjectId(id)})

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('/optech/editoptechc.html', username=session['username'], item=item_per)


    image = request.files["image"]
    cinn = request.form.get('cinn')
    mongo.db.list.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": 
            {'gov': request.form.get('gov'),
            'cin': request.form.get('cin'),
            'cinn': request.form.get('cinn'),
            "doc": request.form.get('doc'),
            "mobiles": request.form.get('mobiles'),
            "rxfb": request.form.get('rxfb'),
            "rxtlg": request.form.get('rxtlg'),
            "rxwa": request.form.get('rxwa'),
            "appareil": request.form.get('appareil'),
            "autres": request.form.get('autres'),
            "sd": request.form.get('sd')   
                    }
        })
    folder = os.path.join("/home/devops/Bureau/unict_app/codzz/app/static/uploads",cinn)
    
    if not request.files["image"].filename == '':
        if (os.path.isdir(folder)):
            #os.removedirs(folder)80
            shutil.rmtree(folder)
            os.makedirs(folder) 
            image.save(os.path.join(folder,(cinn+".jpg")))  
            print("exist")
        else:
            (os.path.isdir(folder))
            os.makedirs(folder) 
            image.save(os.path.join(folder,(cinn+".jpg")))
            print("no exist")
           
        flash('تم تعديل المعطيات بنجاح')
    else:
        flash('تم تعديل المعطيات بدون تغيير الصورة')
        

    return redirect(url_for('searchoptech'))


@application.route("/")
def index():
    if 'username' in session:
        
        return redirect(url_for('gohome'))

    return render_template('login.html')

@application.route("/mapoptech")
def mapoptech():
    if 'username' in session:
            start_coords = (33.9540700, 10.7360300)
            folium_map = folium.Map(location=start_coords, zoom_start=5 , height=600)
            folium_map.save('/home/devops/Bureau/unict_app/codzz/app/templates/map.html')
    
            return render_template('/optech/mapoptech.html')
            #return render_template('map.html')
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
   session.pop('email', None)
   session.clear()
   return redirect(url_for('login'))










@application.route('/addk', methods=['POST', 'GET'])
def addk():

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('/optech/addformk.html', username=session['username'])


    
    mongo.db.list_konia.insert(
        
        
            {'cin': request.form.get('cin'),
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            "rq": request.form.get('rq'),
            'konia': request.form.get('konia'), 
            'src': request.form.get('src')     
        })  
    
    
    flash('تم اضــافة المعطيات بنجاح')
    return redirect(url_for('searchk'))


@application.route("/searchk", methods=['POST', 'GET'])
def searchk():
    if 'username' in session:
        if request.method == "POST":
            text = request.form['text']
            listpersonnes = mongo.db.list_konia
            data = listpersonnes.find( { 'konia' :  {'$regex': text} } )
            return render_template('/optech/searchk.html', data=data)
        return render_template('/optech/searchk.html')
    return render_template('login.html')


@application.route('/editk/<id>', methods=['POST', 'GET'])
def editk(id):
    listper = mongo.db.list_konia
    item_per = listper.find_one({'_id': ObjectId(id)})

    if request.method == 'GET':
     if session['username'] is not None:
        return render_template('/optech/editk.html', username=session['username'], item=item_per)

    mongo.db.list_konia.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": 
            {'cin': request.form.get('cin'),
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            "rq": request.form.get('rq'),
            'konia': request.form.get('konia'), 
            'src': request.form.get('src') 
                    }
        })
     
    flash('تم تعديل المعطيات بنجاح')
    return redirect(url_for('searchk'))











































if __name__ == "__main__":
    application.debug = True
    application.run(port=8000)