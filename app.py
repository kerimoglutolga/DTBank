from flask import Flask, request, render_template, url_for
from flask_mysqldb import MySQL
import hashlib

from werkzeug.wrappers import response

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
            mysql.connection.commit()
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
        cur.execute("UPDATE Bindings SET affinity_nM = %s WHERE reaction_id = %s", (affinity, drugbank_id))
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

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/browse/<string:subpath>')
def browse_db(subpath):
    cur = mysql.connection.cursor()
    if subpath == 'users':
        cur.execute('SELECT username, institute FROM User')
        return render_template('view.html', user=True, table=cur.fetchall())
    if subpath == 'proteins':
        cur.execute('SELECT * FROM UniProt')
        return render_template('view.html', prot=True, table=cur.fetchall())
    if subpath == 'sider':
        cur.execute('SELECT S.umls_cui, S.name, group_concat(DS.drugbank_id) FROM SideEffectName S, DrugCausedSideEffect DS \
            WHERE S.umls_cui = DS.umls_cui \
            GROUP BY S.umls_cui, S.name')
        return render_template('view.html', sider=True, table=cur.fetchall())
    if subpath == 'papers':
        cur.execute('SELECT B.doi, B.reaction_id, group_concat(C.username)\
            FROM Bindings B, Contributors C \
            WHERE B.reaction_id = C.reaction_id \
            GROUP BY B.doi, B.reaction_id')
        return render_template('view.html', papers=True, table=cur.fetchall())
    if subpath == 'drugs':
        cur.execute('SELECT D.drugbank_id, D.name, D.description\
            FROM Drug D')
        return render_template('view.html', drugs=True, table=cur.fetchall())
    if subpath == 'drugtarget':
        cur.execute('SELECT I.interactor_id, group_concat(I.interactee_id)\
            FROM Interacts I GROUP BY I.interactor_id')
        return render_template('view.html', interact=True, table=cur.fetchall())


@app.route('/drugs',methods=['GET'])
def drugOptions1():
    return render_template('drugOptions1.html')

@app.route('/drugs/otherOptions',methods=['GET'])
def drugOptions2():
    return render_template('drugOptions2.html')

@app.route('/drugs/searchKeywordInDescription',methods=['GET','POST'])
def searchKeywordInDescription():
    if request.method=='GET':
        keyword='searchKeywordInDescription'
        return render_template('search.html',keyword=keyword)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT drugbank_id,description FROM Drug WHERE description LIKE \'%{}%\'".format(request.form["keyword"]))
        data=cur.fetchall()
        if len(data)==0:
            success=False
        else:
            success=True
        table=('searchKeywordInDescription',data,request.form["keyword"])
        return render_template('viewSearched.html',table=table,success=success)

@app.route('/drugs/filterTargets',methods=['GET','POST'])
def filterTargets():
    if request.method=='GET':
        return render_template('filterTargets.html')
    else:
        cur = mysql.connection.cursor()
        cur.execute("CALL filterTargets('{}','{}',{},{})".format(request.form["drugbank_id"],request.form["measurement"],request.form["min"],request.form["max"]))
        data=cur.fetchall()
        if len(data)==0:
            success=False
        else:
            success=True
        table=('filterTargets',data,request.form["drugbank_id"],request.form["measurement"], request.form["min"],request.form["max"])
        return render_template('viewSearched.html',table=table,success=success)

@app.route('/drugs/viewAllDrugs',methods=['GET'])
def drugsViewAll():
    cur = mysql.connection.cursor()
    cur.execute("SELECT D.drugbank_id, D.name, D.smiles, D.description, T.target_name, group_concat(E.name separator ', ') \
    FROM Drug D, (SELECT drugbank_id,target_name FROM Bindings) T, DrugCausedSideEffect S, SideEffectName E \
    WHERE D.drugbank_id=S.drugbank_id AND D.drugbank_id=T.drugbank_id AND S.umls_cui=E.umls_cui \
    GROUP BY D.drugbank_id, D.name, D.smiles, D.description, T.target_name")
    data=cur.fetchall()
    if len(data)==0:
        success=False
    else:
        success=True
    table=('viewAllDrugs',data)
    return render_template('viewAll.html',table=table,success=success)

@app.route('/drugs/viewOtherOptionsDrugs',methods=['POST'])
def viewDrugInteractionResults():

    if request.form['Type']=='interactions':
        cur = mysql.connection.cursor()
        cur.execute("SELECT I.interactee_id,D.name FROM Interacts I, Drug D WHERE I.interactor_id='{}' AND \
            I.interactee_id=D.drugbank_id".format(request.form['drugbank_id']))
        data=cur.fetchall()
        if len(data)==0:
            success=False
        else:
            success=True
        table=(request.form['Type'], data,request.form['drugbank_id'])
        return render_template('viewSearched.html',table=table,success=success)

    elif request.form['Type']=='side effects':
        cur = mysql.connection.cursor()
        cur.execute("SELECT N.name,S.umls_cui FROM DrugCausedSideEffect S, SideEffectName N WHERE \
            S.drugbank_id='{}' AND S.umls_cui=N.umls_cui".format(request.form['drugbank_id']))
        data=cur.fetchall()
        if len(data)==0:
            success=False
        else:
            success=True
        table=(request.form['Type'], data,request.form['drugbank_id'])
        return render_template('viewSearched.html',table=table,success=success)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT uniprot_id, target_name FROM Bindings WHERE drugbank_id='{}'".format(request.form['drugbank_id']))
        data=cur.fetchall()
        if len(data)==0:
            success=False
        else:
            success=True
        table=(request.form['Type'], data,request.form['drugbank_id'])
        return render_template('viewSearched.html',table=table,success=success)
    
@app.route('/proteins',methods=['GET'])
def proteinsOptions():
    return render_template('proteins.html')

@app.route('/proteins/searchProtein',methods=['GET'])
def searchProtein():
    keyword='searchProtein'
    return render_template('search.html',keyword=keyword)

@app.route('/proteins/drugsForSameProtein',methods=['GET'])
def drugsForSameProtein():
    cur = mysql.connection.cursor()
    cur.execute("SELECT U.uniprot_id,GROUP_CONCAT(DISTINCT B.drugbank_id) FROM \
        UniProt U LEFT JOIN Bindings B ON U.uniprot_id=B.uniprot_id GROUP BY U.uniprot_id")
    data=cur.fetchall()
    if len(data)==0:
        success=False
    else:
        success=True
    table=('drugsForSameProtein', data)
    return render_template('viewAll.html',table=table,success=success)

@app.route('/proteins/proteinsForSameDrug',methods=['GET'])
def proteinsForSameDrug():
    cur = mysql.connection.cursor()
    cur.execute("SELECT D.drugbank_id,GROUP_CONCAT(DISTINCT B.uniprot_id) FROM \
    Drug D LEFT JOIN Bindings B ON B.drugbank_id=D.drugbank_id GROUP BY D.drugbank_id")
    data=cur.fetchall()
    if len(data)==0:
        success=False
    else:
        success=True
    table=('proteinsForSameDrug',data)
    return render_template('viewAll.html',table=table,success=success)

@app.route('/proteins/aProteinInteractedDrugs',methods=['POST'])
def aProteinInteractedDrugs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT D.drugbank_id,D.name FROM Bindings B,Drug D \
        WHERE B.uniprot_id='{}' AND D.drugbank_id=B.drugbank_id GROUP BY D.drugbank_id,D.name".format(request.form['uniprot_id']))
    data=cur.fetchall()
    if len(data)==0:
        success=False
    else:
        success=True
    table=('aProteinInteractedDrugs', data,request.form['uniprot_id'])
    return render_template('viewSearched.html',table=table,success=success)

@app.route('/sider',methods=['GET','POST'])
def sider():
    if request.method=='GET':
        return render_template("sider.html")
    else:
        if request.form["Type"]=='drugsWithSameSider':
            cur = mysql.connection.cursor()
            cur.execute("SELECT D.drugbank_id, D.name FROM DrugCausedSideEffect S, Drug D \
            WHERE D.drugbank_id=S.drugbank_id AND S.umls_cui='{}'".format(request.form["keyword"]))
            data=cur.fetchall()
            if len(data)==0:
                success=False
            else:
                success=True
            table=('aSiderForDrugs',data,request.form["keyword"])
            return render_template('viewSearched.html',table=table,success=success)
        else:
            cur = mysql.connection.cursor()
            """cur.execute("SELECT D.drugbank_id, D.name FROM \
            (SELECT COUNT(B.drugbank_id) AS number,B.drugbank_id FROM \
            (SELECT uniprot_id, drugbank_id FROM Bindings GROUP BY uniprot_id, drugbank_id) AS B,DrugCausedSideEffect S \
            WHERE B.drugbank_id=S.drugbank_id AND B.uniprot_id='{}'  \
            GROUP BY B.drugbank_id) AS T, Drug D \
            WHERE T.drugbank_id=D.drugbank_id AND T.number=(SELECT min(T.number) FROM \
            (SELECT COUNT(B.drugbank_id) AS number,B.drugbank_id FROM \
            (SELECT uniprot_id, drugbank_id FROM Bindings GROUP BY uniprot_id, drugbank_id) AS B,DrugCausedSideEffect S \
            WHERE B.drugbank_id=S.drugbank_id AND B.uniprot_id='u' \
            GROUP BY B.drugbank_id) AS T)".format(request.form["keyword"]))"""

            cur.execute("SELECT D.drugbank_id, D.name FROM Drug D, \
            (SELECT X.drugbank_id FROM (SELECT drugbank_id, COUNT(*) AS secount FROM drugcausedsideeffect  \
            WHERE drugbank_id IN (SELECT drugbank_id FROM Bindings WHERE uniprot_id = %s GROUP BY drugbank_id) GROUP BY drugbank_id) AS X \
            WHERE X.secount = (SELECT MIN(T.secount) FROM (SELECT drugbank_id, COUNT(*) AS secount FROM drugcausedsideeffect  \
            WHERE drugbank_id IN (SELECT drugbank_id FROM Bindings WHERE uniprot_id = %s GROUP BY drugbank_id) GROUP BY drugbank_id) AS T)) as Y \
            WHERE D.drugbank_id = Y.drugbank_id", (request.form["keyword"], request.form["keyword"]))
            data=cur.fetchall()
            if len(data)==0:
                success=False
            else:
                success=True
            table=('drugLeastSider',data,request.form["keyword"])
            return render_template('viewSearched.html',table=table,success=success)

@app.route('/doi',methods=['GET'])
def doi():
    cur = mysql.connection.cursor()
    cur.execute("select B.doi, group_concat(distinct U.name separator ';') \
    FROM Bindings B, (SELECT reaction_id,username FROM Contributors) C, User U \
    WHERE B.reaction_id=C.reaction_id AND U.username=C.username\
    GROUP BY B.doi")
    data=cur.fetchall()
    if len(data)==0:
        success=False
    else:
        success=True
    table=('doi',data)
    return render_template('viewAll.html',table=table,success=success)

@app.route('/institutes',methods=['GET'])
def institutes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Points ORDER BY score DESC")
    data=cur.fetchall()
    if len(data)==0:
        success=False
    else:
        success=True
    table=('institutes',data)
    return render_template('viewAll.html',table=table,success=success)



if __name__ == "__main__":
    app.run(debug=True)