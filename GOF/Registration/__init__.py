from sre_constants import SUCCESS
from unicodedata import name
from flask import render_template, Blueprint, request, redirect, session, flash
from datetime import datetime
import hashlib
import os
from werkzeug.utils import secure_filename
from pathlib import Path

registration = Blueprint('registration', __name__)

from ..extensions import mongo
print(mongo)
users = mongo.db.Users
qna_database = mongo.db.QnA

location = os.path.join(Path(__file__).parent.parent,Path('static/files'))
print("Loaction_ regisration:", location)

@registration.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        uname = request.form.get('username')
        pwd = request.form.get('password')
        hash_pwd = hashlib.md5(pwd.encode()).hexdigest()
        login_user = users.find_one({'_id': uname, 'password': hash_pwd})
        if login_user:
            flash("Successfully logged in !")
            session['username'] = uname
            return redirect("/")
        else:
            flash("Please Check Username/Password !")
    return render_template('Registration/login.html', name='login')


@registration.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == "POST":
        uname = request.form.get('username')
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        number = request.form.get('phonenumber')
        occupation = request.form.get('occupation')
        college = request.form.get('college')
        pass_ = request.form.get('password')
        hash_pwd = hashlib.md5(pass_.encode()).hexdigest()
        age = request.form.get('age')
        email = request.form.get('email')
        file = request.files.getlist('profile_pic')
        if len(file[0].filename)!=0:
            file = file[0]
            file.save(os.path.join(os.path.abspath(location),secure_filename(file.filename))) 
            dict_ = {
            "_id": uname,
            "firstname": fname,
            "lastname": lname,
            "phonenumber": number,
            "email": email,
            "occupation": occupation,
            "college": college,
            "password": hash_pwd,
            "age": age,
            "signupdate": datetime.now(),
            "file": secure_filename(file.filename)
            }    
        else:
            dict_ = {
                "_id": uname,
                "firstname": fname,
                "lastname": lname,
                "phonenumber": number,
                "email": email,
                "occupation": occupation,
                "college": college,
                "password": hash_pwd,
                "age": age,
                "signupdate": datetime.now(),
                "file": ""
            }

        login_user = users.find_one({'_id': uname})
        phone_user = users.find_one({'phonenumber': number})
        email_user = users.find_one({'email': email})
        if login_user:
            flash('Username already exists !')
            return redirect('/registration/signup')
        elif phone_user:
            flash('Mobile number already exists !')
            return redirect('/registration/signup')
        elif email_user:
            flash('E-mail already exists !')
            return redirect('/registration/signup')
        else:
            users.insert_one(dict_)
            session['username'] = uname
            flash('You successfully registered !')
            return redirect('/')
    return render_template('Registration/signup.html', name='signup')


@registration.route('/profile/<id>')
def profile(id):
    if not session:
        return redirect('/registration/')
    user = users.find_one({'_id': id})
    ques = qna_database.find({'user_id':id})
    return render_template('Registration/profile.html', name='profile', data = user, ques=ques)


@registration.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@registration.route('/update/<id>', methods=['GET','POST'])
def update(id):
    if session['username'] != id:
        flash('Please SignIn as '+id)
        return redirect('/')
    user = users.find_one({'_id': id})
    if request.method == 'POST':
        uname = request.form.get('username')
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        number = request.form.get('phonenumber')
        occupation = request.form.get('occupation')
        college = request.form.get('college')
        age = request.form.get('age')
        email = request.form.get('email')
        file = request.files.getlist('profile_pic')
        print(file)
        if len(file[0].filename)!=0:
            file = file[0]
            file.save(os.path.join(os.path.abspath(location),secure_filename(file.filename))) 
            dict_ = {
            "_id": uname,
            "firstname": fname,
            "lastname": lname,
            "phonenumber": number,
            "email": email,
            "occupation": occupation,
            "college": college,
            "password": user['password'],
            "age": age,
            "signupdate": datetime.now(),
            "file": secure_filename(file.filename)
            }    
        else:
            dict_ = {
                "_id": uname,
                "firstname": fname,
                "lastname": lname,
                "phonenumber": number,
                "email": email,
                "occupation": occupation,
                "college": college,
                "password": user['password'],
                "age": age,
                "signupdate": datetime.now(),
                "file": user['file']
            }
        users.update_one({'_id':id}, {'$set':dict_})
        return redirect('/registration/profile/'+id)
    return render_template('Registration/update_profile.html', name='update_profile', data = user)
