from flask import Flask, render_template, url_for, request, redirect, session
import pymysql as sql
import re
from datetime import date
from flask_wtf import FlaskForm
from wtforms.fields import DateField, EmailField, TelField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
date.fromisoformat('2019-12-04')

app = Flask(__name__)
db = sql.connect(
    host="pf.c7wjaspqw9qm.us-east-1.rds.amazonaws.com",
    user="root",
    password="AWSPassword"
)

app.secret_key = 'super secret key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        #cursor = sql.connection.cursor(db.cursors.DictCursor)
        cursor.execute('use pf2')
        #cursor.execute('SELECT * FROM PUser')
        #cursor.execute('SELECT * FROM PUser WHERE email = % s AND password = % s', ('NULL', 'NULL', 'NULL',email, 55-55-1977, 'F', password))
        cursor.execute('SELECT * FROM PUser WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['email'] = user[3]
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

class InfoForm(FlaskForm):
    startdate = DateField('BirthDate', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

# @app.route('/register')
# def register():
#     if request.method == 'GET':
#         return render_template("register.html")
#     else:
#         name = request. form['name']
#         email = request.form['email']
#         PUsername = request. form['username']
#         FName = request.form['fristName']
#         LName = request.form['lastName']
#         password = request.form['password'].encode('utf-8')

#         cur = sql.connection.cursor()
#         cur.execute("INSERT INTO PUser (name, email, password) VALUES (%s,%s,%s)", (name, email, password,))
#         sql.connection.commit()
#         session['name'] = name
#         session['email'] = email
#     return redirect(url_for("home"))

# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     mesage = ''
#     if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
#         userName = request.form['name']
#         password = request.form['password']
#         email = request.form['email']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
#         account = cursor.fetchone()
#         if account:
#             mesage = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             mesage = 'Invalid email address !'
#         elif not userName or not password or not email:
#             mesage = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
#             mysql.connection.commit()
#             mesage = 'You have successfully registered !'
#     elif request.method == 'POST':
#         mesage = 'Please fill out the form !'
#     return render_template('register.html', mesage = mesage)

@app.route('/register', methods=['GET','POST'])
def register():
    mesage=''
    print('herrr')
    form = InfoForm()
    print('heeyy')
    if request.method == 'POST' :
        print('ff')
        email = request.form['email']
        print('email is ',email)
        PUsername = request. form['username']
        print('username is ',PUsername)
        FName = request.form['firstName']
        LName = request.form['lastName']
        gender = request.form['gender']
        Birthdate = request.form['birthdate']
        password = request.form['password'].encode('utf-8')

        cur = db.cursor()
        cur.execute('use pf2')
        cur.execute('SELECT * FROM PUser WHERE email = % s', (email, ))
        account = cur.fetchone()

        cur.execute("INSERT INTO PUser (Username, FName, LName, Email, Birthdate, gender, UPassword) VALUES ('newwwwww', 'FName', 'LName', 'email', '1999-09-09','F', 'password')");
        db.commit
        cur.execute("SELECT * FROM PUser where email='email'")
        xd = cur.fetchone()
        print(xd)

        if account:
            mesage = 'Account already exists !'
            print('here1')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
            print('here2')
        elif not PUsername or not password or not email:
            mesage = 'Please fill out the form !'
            print('here3')
        else:
            print('in hereeeee')
            cur.execute("INSERT INTO PUser (Username, FName, LName, Email, Birthdate, gender, UPassword) VALUES (%s,%s,%s, %s,%s,%s, %s)", (PUsername, FName, LName, email, Birthdate,gender, password,))
            db.commit()
            
            print('you have sucessfully')
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'

        # sql.connection.commit()
        # session['name'] = name
        # session['email'] = email
        # session['startdate'] = form.startdate.data
        # session['enddate'] = form.enddate.data
        # return redirect(url_for("home"))
    return render_template('register.html', form=form)
cur = db.cursor()

if __name__ =="__main__":
    # cur.execute('use pf2')
    # cur.execute("SELECT * FROM PUser")
    # xd = cur.fetchall()
    # for xdd in xd:
    #     print(xdd)
    app.run(debug=True)
    