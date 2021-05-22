from flask import Flask, request, render_template, url_for
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def login():
    username = request.form['Username']
    password = request.form['Password']
    type = request.form['Type']

    con = sqlite3.connect('DTBank.db')
    cur = con.cursor()

    if type == 'User':
        cur.execute('SELECT EXISTS(SELECT 1 FROM User WHERE username=? \
            AND password = ?)', (username, password))
        rc = int(cur.fetchone()[0])
        if rc:
            return render_template('user.html', username=username)
        else: return render_template('login_error.html')
    elif type == 'Manager':
        cur.execute('SELECT EXISTS(SELECT 1 FROM DatabaseManager WHERE username=? \
            AND password = ?)', (username, password))
        rc = int(cur.fetchone()[0])
        if rc:
            return render_template('manager.html', username=username)
        else: return render_template('login_error.html')

@app.route('/adduser', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('adduser.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        institute = request.form['Institute']
        return render_template('manager.html', added_user=True)


@app.route('/user')
def logged_in():
    return render_template('user.html', username="Tolga")

@app.route('/drugs')
def drugs():
    con = sqlite3.connect('DTBank.db')
    cur = con.cursor()
    cur.execute("SELECT D.name, D.drugbank_id, DC.smiles, D.description, B.target_name, group_concat(S.name) \
        FROM Drug D, DrugCausedSideEffect DS, SideEffectName S, DrugChemicalNotations DC, Bindings B \
        WHERE D.drugbank_id = B.drugbank_id AND D.drugbank_id = DC.drugbank_id AND D.drugbank_id = DS.drugbank_id \
        GROUP BY D.name, D.drugbank_id, DC.smiles, D.description, B.target_name")
    rows = cur.fetchall()
    return render_template('drugs.html', rows=rows)

if __name__ == "__main__":
    app.run(debug=True)