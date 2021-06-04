import xlrd 

import MySQLdb

# To run the following script, you need to have an active MySQL server running locally. 
 # Enter your password and database name for the last two parameters, respectively

con = MySQLdb.connect('localhost', 'root', 'group4','dtbank')
cur = con.cursor()

loc = ("data.xls")

wb = xlrd.open_workbook(loc)


for i in range(1,8):
    sheet = wb.sheet_by_index(0)
    username = sheet.row_slice(i, 1,4)
    username, institute, password = tuple([field.value for field in sheet.row_slice(i, 1, 4)])
    cur.execute("INSERT INTO User(username, institute, password) \
        VALUES (%s, %s, %s)", (username, institute, password))
    con.commit()

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
    con.commit()

sheet=wb.sheet_by_index(2)
print(sheet.cell_value(1,9))
for i in range(1,18):
    bindingdb=sheet.row_slice(i,0,10)
    reaction_id,drugbank_id,uniprot_id,target_name, smiles,measure,affinity_nM,doi,authors,institute=sheet.row_slice(i,0,10)
    cur.execute("SELECT * FROM User")
    users=
    cur.execute("INSERT INTO Bindings VALUES(%s,%s,%s,%s,%s,%s,%s)",(reaction_id,measure,int(affinity_nM),doi,drugbank_id,uniprot_id,target_name,institute))"""
    