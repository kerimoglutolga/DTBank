import xlrd 

import MySQLdb
import hashlib
# To run the following script, you need to have an active MySQL server running locally. 
 # Enter your password and database name for the last two parameters, respectively

con = MySQLdb.connect('localhost', 'root', 'group4','dtbank')
cur = con.cursor()

loc = ("data.xls")

wb = xlrd.open_workbook(loc)


"""for i in range(1,8):
    sheet = wb.sheet_by_index(0)
    username = sheet.row_slice(i, 1,4)
    username, institute, password = tuple([field.value for field in sheet.row_slice(i, 1, 4)])
    cur.execute("INSERT INTO User(username, institute, password) \
        VALUES (%s, %s, %s)", (username, institute, password))
    con.commit()"""

"""for i in range(1,4):
    sheet = wb.sheet_by_index(1)
    username, password = tuple([field.value for field in sheet.row_slice(i, 0, 2)])
    cur.execute("INSERT INTO DatabaseManager \
        VALUES (%s, %s)", (username, password))
    con.commit()"""

"""for i in range(1,10):
    sheet = wb.sheet_by_index(5)
    uniprot_id, seq= tuple([field.value for field in sheet.row_slice(i, 0, 2)])
    cur.execute("INSERT INTO UniProt \
        VALUES (%s, %s)", (uniprot_id, seq))
    con.commit()"""

"""for i in range(1,10):
    sheet = wb.sheet_by_index(5)
    uniprot_id, seq= tuple([field.value for field in sheet.row_slice(i, 0, 2)])
    cur.execute("INSERT INTO UniProt \
        VALUES (%s, %s)", (uniprot_id, seq))
    con.commit()"""

"""for i in range(1,13):
    sheet = wb.sheet_by_index(3)
    drugbank_id, name, description = tuple([field.value for field in sheet.row_slice(i, 0, 3)])
    sheet = wb.sheet_by_index(2)
    for row in sheet.get_rows():
        if row[1].value == drugbank_id:
            cur.execute('INSERT IGNORE INTO Drug \
                VALUES(%s, %s, %s, %s)', (drugbank_id, name,description, row[4].value))
            con.commit()"""

"""for i in range(1,18):
    sheet = wb.sheet_by_index(2)
    reaction_id, drugbank_id, uniprot_id, target_name, smiles, measure, affinity, doi, authors, institute = tuple([field.value for field in sheet.row_slice(i, 0, 10)])
    cur.execute("INSERT INTO Bindings \
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (int(reaction_id), measure, int(affinity), doi, drugbank_id, uniprot_id, target_name, institute))
    con.commit()"""

"""for i in range(1,18):
    sheet = wb.sheet_by_index(2)
    reaction_id, _, _, _, _, _, _, _, authors, institute = tuple([field.value for field in sheet.row_slice(i, 0, 10)])
    authors = authors.split("; ")
    sheet = wb.sheet_by_index(0)
    for author in authors:
        for row in sheet.get_rows():
            if (row[0].value == author):
                cur.execute("INSERT IGNORE INTO Contributors \
                    VALUES(%s, %s, %s)", (reaction_id, row[1].value, institute))
    con.commit()"""

"""sheet=wb.sheet_by_index(4)
for i in range(1,79):
    umls_cui,drugbank_id,side_effect_name=tuple([field.value for field in sheet.row_slice(i,0,3)])
    cur.execute("insert ignore into SideEffectName values (%s, %s)",(umls_cui,side_effect_name))
    cur.execute("insert ignore into DrugCausedSideEffect values(%s,%s)",(umls_cui,drugbank_id))
    con.commit()"""
    
"""cur.execute("SELECT * FROM User")
res = cur.fetchall()
for row in res:
    hashed_pw = hashlib.sha256(row[2].encode()).hexdigest()
    cur.execute("UPDATE User SET password = %s WHERE username = %s AND institute = %s", (hashed_pw, row[0], row[1]))"""
    

