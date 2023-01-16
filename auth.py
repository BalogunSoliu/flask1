from flask import Blueprint,render_template,request,flash,url_for,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_required, logout_user,login_user,current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password1']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password, try again', category='error')
        else:
            flash('user doesn\'t exist, sign up', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required #meaning, you are required to login, to be eligible to logout
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method=='POST':
        email = request.form['email']
        firstname=request.form['firstName']
        password1=request.form['password1']
        password2=request.form['password2']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist')
        elif len(email) < 4:
            flash('Email must be greater than four.', category='error')
        elif len(firstname) < 2:
            flash('Firstname must be greater than two characters.', category='error')
        elif password1!=password2:
            flash('passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('password must be greater than seven characters.', category='error')
        else:
            new_user=User(email=email, password=generate_password_hash(password1, method='sha256'),first_name=firstname)
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!', category='success')
            login_user(user,remember=True)
            return redirect(url_for('views.home'))
            

    return render_template('signup.html',user=current_user)