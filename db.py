import MySQLdb

# To run the following script, you need to have an active MySQL server running locally. 
con = MySQLdb.connect('localhost', 'root', 'group4', 'dtbank') # Enter your password and database name for the last two parameters, respectively

cur = con.cursor()

# Following code creates the refined tables

"""cur.execute("CREATE TABLE User( \
    username VARCHAR(30), \
    institute VARCHAR(100), \
    password CHAR(64), \
    PRIMARY KEY(username,institute))")"""

"""cur.execute("CREATE TABLE DatabaseManager(\
    username VARCHAR(30), \
    password VARCHAR(64), \
    PRIMARY KEY(username))")"""

"""cur.execute("CREATE TABLE UniProt( \
    uniprot_id CHAR(6), \
    sequence TEXT, \
    PRIMARY KEY(uniprot_id))")"""

"""cur.execute("CREATE TABLE Drug( \
    drugbank_id CHAR(7), \
    name VARCHAR(30), \
    description TEXT,
    smiles VARCHAR(200), \
    PRIMARY KEY(drugbank_id), \
    UNIQUE(name), \
    UNIQUE(smiles))")"""

"""cur.execute("CREATE TABLE Interacts ( \
    interactor_id VARCHAR(30), \
    interactee_id VARCHAR(30), \
    PRIMARY KEY(interactor_id,interactee_id), \
    FOREIGN KEY (interactor_id) REFERENCES Drug(drugbank_id) ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (interactee_id) REFERENCES Drug(drugbank_id) ON DELETE CASCADE ON UPDATE CASCADE)")"""

"""cur.execute("CREATE TABLE SideEffectName( \
    umls_cui CHAR(8), \
    name VARCHAR(30), \
    PRIMARY KEY(umls_cui), \
    UNIQUE(name))")"""

"""cur.execute("CREATE TABLE DrugCausedSideEffect( \
    umls_cui CHAR(8), \
    drugbank_id CHAR(7), \
    PRIMARY KEY(umls_cui,drugbank_id), \
    FOREIGN KEY (drugbank_id) REFERENCES Drug(drugbank_id) ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (umls_cui) REFERENCES SideEffectName(umls_cui) ON DELETE CASCADE ON UPDATE CASCADE)")"""



"""cur.execute("CREATE TABLE Bindings( \
    reaction_id INTEGER, \
    measure VARCHAR(4), \
    affinity_nM INTEGER, \
    doi VARCHAR(50), \
    drugbank_id CHAR(7), \
    uniprot_id CHAR(6), \
    username VARCHAR(30), \
    institute VARCHAR(100), \
    target_name VARCHAR(100), \
    PRIMARY KEY(reaction_id), \
    FOREIGN KEY (drugbank_id) REFERENCES Drug(drugbank_id) ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (uniprot_id) REFERENCES UniProt(uniprot_id) ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (username,institute) REFERENCES User(username, institute) ON DELETE CASCADE ON UPDATE CASCADE)")"""

"""cur.execute("CREATE TABLE Contributors( \
    reaction_id INTEGER, \
    username VARCHAR(30), \
    institute VARCHAR(100), \
    PRIMARY KEY (reaction_id, username), \
    FOREIGN KEY (reaction_id) REFERENCES Bindings(reaction_id) ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (username, institute) REFERENCES User(username, institute) ON DELETE CASCADE ON UPDATE CASCADE)")"""

"""cur.execute("CREATE TABLE Points( \
    institute VARCHAR(100), \
    score INTEGER, \
    PRIMARY KEY (institute))")"""


# To do 1: Add the triggers
# To do 2: Enforce the constraint that the DatabaseManager table can have at most 5 entries

