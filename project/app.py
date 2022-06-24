from flask import Flask, redirect, render_template, url_for, request, session
import pymysql


connection = pymysql.connect (
    host = 'localhost',
    port =  3306,
    database = 'crud',
    user = 'root',
    password = ''
)

cursor = connection.cursor()
app = Flask (__name__)
app.secret_key = 'super secret key'

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html', username = session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST':
        username= request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM user WHERE username = %s AND password=%s',(username,password))
        row= cursor.fetchone()
        if row:
            session['loggedin']= True
            session['username'] =  row[1]
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password'
    return render_template('index.html',msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username', None)

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)