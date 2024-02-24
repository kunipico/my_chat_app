from flask import Flask,render_template,request,flash,session,redirect
import re
import uuid
import hashlib
from util.user import User 
from models import dbConnect
from datetime import timedelta


###################
# Initialization  #
###################
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=1)

@app.get('/')
def hello_world():
    print('Hello Flask!')
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        return "<p>Hello, World!</p>"


@app.get('/login')
def login():
    return render_template('login.html')

@app.post('/login')
def userlogin():
    name = request.form.get('name')
    password = request.form.get('password')
    if name =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUser(name)
        if user is None:
            flash('ログイン情報が間違っています')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('ログイン情報が間違っています')
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')



@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.post('/signup')
def userSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('newPassword')
    password2 = request.form.get('confPassword')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email =='' or password1 == '' or password2 == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        user = User(uid, name, email, password)
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(user)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')


if __name__ == '__main__':
    app.run(debug=True,port='8080')