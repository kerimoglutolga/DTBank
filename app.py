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
        cur.execute('SELECT COUNT(1) FROM DatabaseManager DM WHERE DM.username = %s AND DM.password = %s', (username, hashed_pw))
        rc = int(cur.fetchone()[0]) # return code
        con.commit()
        if rc: return render_template('manager.html', username=username)
        return render_template('login_error.html')
    elif type == 'User': 
        cur.execute('SELECT COUNT(1) FROM User U WHERE U.username = %s AND U.password = %s', (username, hashed_pw))
        rc = int(cur.fetchone()[0]) # return code
        con.commit()
        if rc: return render_template('user.html', username=username)
        return render_template('login_error.html')
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
        try:
            cur.execute("INSERT INTO User(username, password, institute) \
            VALUES (%s, %s, %s)", params)
        except mysql.connection.Error as err:
            return render_template('adduser.html', error=True)
        return render_template('manager.html', added_user=True)

@app.route('/deletedrugs', methods = ['GET', 'POST'])
def delete_drug():
    # TODO: Add a check for whether the user is already registered or not
    if request.method == 'GET':
        return render_template('editdrugs.html', delete=True)
    elif request.method == 'POST':
        drugbank_id = request.form['drugid']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Drug WHERE drugbank_id = %s", (drugbank_id,))
        cur.execute("SELECT ROW_COUNT()")
        rc = int(cur.fetchone()[0])
        mysql.connection.commit()
        if rc:
            return render_template('editdrugs.html', delete=True, success=True)
        else: return render_template('editdrugs.html', delete=True, success=False)

@app.route('/affinity', methods = ['GET', 'POST'])
def update_drug():
    # TODO: Add a check for whether the user is already registered or not
    if request.method == 'GET':
        return render_template('editdrugs.html', affinity=True)
    elif request.method == 'POST':
        drugbank_id = request.form['drugid']
        affinity = request.form['affinity']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Bindings SET affinity_nM = %s WHERE drugbank_id = %s", (affinity, drugbank_id))
        cur.execute("SELECT ROW_COUNT()")
        rc = int(cur.fetchone()[0])
        mysql.connection.commit()
        if rc:
            return render_template('editdrugs.html', affinity=True, success=True)
        else: return render_template('editdrugs.html', affinity=True, success=False)

@app.route('/deleteprot', methods = ['GET', 'POST'])
def delete_prot():
    if request.method == 'GET':
        return render_template('prot.html')
    elif request.method == 'POST':
        uniprot_id = request.form['protid']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM UniProt WHERE uniprot_id = %s", (uniprot_id,))
        cur.execute("SELECT ROW_COUNT()")
        rc = int(cur.fetchone()[0])
        mysql.connection.commit()
        if rc:
            return render_template('prot.html', success=True)
        else: return render_template('prot.html', success=False)

@app.route('/updatecontrib', methods = ['GET', 'POST'])
def contrib():
    if request.method == 'GET':
        return render_template('updatecontrib.html')
    elif request.method == 'POST':
        reaction_id = request.form['reactionid']
        username = request.form['contrib']
        institute = request.form['institute']
        cur = mysql.connection.cursor()
        rc = 1
        if 'delete' in request.form:
            cur.execute("DELETE FROM Contributors \
                WHERE reaction_id = %s AND username = %s AND institute = %s", (reaction_id, username, institute))
            cur.execute("SELECT ROW_COUNT()")
            rc = int(cur.fetchone()[0])
        if 'add' in request.form:
            try:
                cur.execute("INSERT INTO Contributors (reaction_id, username, institute) \
                VALUES (%s, %s, %s)", (reaction_id, username, institute))
            except mysql.connection.Error as err:
                rc = 0       
        mysql.connection.commit()
        if rc:
            return render_template('updatecontrib.html', success=True)
        else: return render_template('updatecontrib.html', success=False)

@app.route('/drugs',methods=['GET'])
def drugOptions1():
    return render_template('drugOptions1.html')

@app.route('/drugs/otherOptions',methods=['GET'])
def drugOptions2():
    return render_template('drugOptions2.html')

@app.route('/drugs/viewAllDrugs',methods=['GET'])
def drugsViewAll():
    cur = mysql.connection.cursor()
    cur.execute("SELECT D.drugbank_id, D.name, D.smiles, D.description, T.target_name, E.name \
    FROM Drug D, (SELECT drugbank_id,target_name FROM Bindings) T, DrugCausedSideEffect S, SideEffectName E \
    WHERE D.drugbank_id=S.drugbank_id AND D.drugbank_id=T.drugbank_id AND S.umls_cui=E.umls_cui")
    table=('viewAllDrugs',cur.fetchall())
    return render_template('viewAll.html',table=table)

@app.route('/drugs/viewOtherOptionsDrugs',methods=['POST'])
def viewDrugInteractionResults():

    if request.form['Type']=='interactions':
        cur = mysql.connection.cursor()
        cur.execute("SELECT I.interactee_id,D.name FROM Interacts I, Drug D WHERE I.interactor_id=%s AND \
            I.interactee_id=D.drugbank_id",request.form['drugbank_id'])
        table=(request.form['Type'], cur.fetchall(),request.form['drugbank_id'])
        return render_template('viewSearched.html',table=table)

    elif request.form['Type']=='side effects':
        cur = mysql.connection.cursor()
        cur.execute("SELECT N.name,S.umls_cui FROM DrugCausedSideEffect S, SideEffectName N WHERE \
            S.drugbank_id=%s AND S.umls_cui=N.umls_cui",request.form['drugbank_id'])
        table=(request.form['Type'], cur.fetchall(),request.form['drugbank_id'])
        return render_template('viewSearched.html',table=table)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT uniprot_id, target_name FROM Bindings WHERE drugbank_id=%s",request.form['drugbank_id'])
        table=(request.form['Type'], cur.fetchall(),request.form['drugbank_id'])
        return render_template('viewSearched.html',table=table)
    
@app.route('/proteins',methods=['GET'])
def proteinsOptions():
    return render_template('proteins.html')

@app.route('/proteins/searchProtein',methods=['GET'])
def searchProtein():
    return render_template('searchProtein.html')

@app.route('/proteins/drugsForSameProtein',methods=['GET'])
def drugsForSameProtein():
    cur = mysql.connection.cursor()
    cur.execute("SELECT U.uniprot_id,GROUP_CONCAT(DISTINCT B.drugbank_id) FROM \
        UniProt U LEFT JOIN Bindings B ON U.uniprot_id=B.uniprot_id GROUP BY U.uniprot_id")
    table=('drugsForSameProtein', cur.fetchall())
    return render_template('viewAll.html',table=table)

@app.route('/proteins/proteinsForSameDrug',methods=['GET'])
def proteinsForSameDrug():
    cur = mysql.connection.cursor()
    cur.execute("SELECT D.drugbank_id,GROUP_CONCAT(DISTINCT B.uniprot_id) FROM \
    Drug D LEFT JOIN Bindings B ON B.drugbank_id=D.drugbank_id GROUP BY D.drugbank_id")
    table=('proteinsForSameDrug',cur.fetchall())
    return render_template('viewAll.html',table=table)

@app.route('/proteins/aProteinInteractedDrugs',methods=['POST'])
def aProteinInteractedDrugs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT D.drugbank_id,D.name FROM Bindings B,Drug D \
        WHERE B.uniprot_id=%s AND D.drugbank_id=B.drugbank_id GROUP BY D.drugbank_id,D.name",request.form['uniprot_id'])
    table=('aProteinInteractedDrugs', cur.fetchall(),request.form['uniprot_id'])
    return render_template('viewSearched.html',table=table)

if __name__ == "__main__":
    app.run(debug=True)