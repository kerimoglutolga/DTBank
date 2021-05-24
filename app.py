from flask import Flask, request, render_template, url_for
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'group4'
app.config['MYSQL_DB'] = 'dtbank'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def login():
    username = request.form['Username']
    hashed_pw = hashlib.sha256(request.form['Password'].encode()).hexdigest()
    type = request.form['Type']
    con = mysql.connection
    cur = con.cursor()
    if type == 'Manager':
        cur.execute('SELECT * FROM DatabaseManager DM WHERE DM.username = %s AND DM.password = %s', (username, hashed_pw))
    if type == 'User': 
        cur.execute('SELECT COUNT(1) FROM User U WHERE U.username = %s AND U.password = %s', (username, hashed_pw))
    rc = int(cur.fetchone()[0]) # return code
    if rc: 
        return render_template('user.html', username=username)
    else: return render_template('login_error.html')


@app.route('/adduser', methods = ['GET', 'POST'])
def add_user():
    # TODO: Add a check for whether the user is already registered or not
    if request.method == 'GET':
        return render_template('adduser.html')
    else:
        hashed_pw = hashlib.sha256(request.form['Password'].encode()).hexdigest()
        params =  (request.form['Username'], hashed_pw, request.form['Institute'])
        print(params)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO User(username, password, institute) \
            VALUES (%s, %s, %s)", params)
        mysql.connection.commit()
        return render_template('manager.html', added_user=True)


if __name__ == "__main__":
    app.run(debug=True)