import sqlite3

con = sqlite3.connect('DTBank.db')

cur = con.cursor()

# Following code creates the refined tables

"""cur.execute("CREATE TABLE User( \
    username TEXT, \
    institute TEXT, \
    password TEXT, \
    PRIMARY KEY(username,institute))")"""

"""cur.execute("CREATE TABLE DatabaseManager(\
    username TEXT, \
    password TEXT, \
    PRIMARY KEY(username))")"""

"""cur.execute("CREATE TABLE UniProt( \
    uniprot_id TEXT, \
    sequence TEXT, \
    PRIMARY KEY(uniprot_id), \
    UNIQUE(sequence))")"""

"""cur.execute("CREATE TABLE Interacts ( \
    interactor_id TEXT, \
    interactee_id TEXT, \
    PRIMARY KEY(interactor_id,interactee_id), \
    FOREIGN KEY (interactor_id) REFERENCES Drug ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (interactee_id) REFERENCES Drug ON DELETE CASCADE ON UPDATE CASCADE)")"""

"""cur.execute("CREATE TABLE DrugCausedSideEffect( \
    umls_cui TEXT, \
    drugbank_id TEXT, \
    PRIMARY KEY(umls_cui,drugbank_id), \
    FOREIGN KEY (drugbank_id) REFERENCES Drug ON DELETE CASCADE ON UPDATE CASCADE)")"""

"""cur.execute("CREATE TABLE SideEffectName( \
    umls_cui TEXT, \
    name TEXTs, \
    PRIMARY KEY(umls_cui), \
    UNIQUE(name))")"""

"""cur.execute("CREATE TABLE Bindings( \
    reaction_id INTEGER, \
    measure TEXT, \
    affinity_nM INTEGER, \
    doi TEXT, \
    drugbank_id TEXT, \
    uniprot_id TEXT, \
    username TEXT, \
    institute TEXT, \
    target_name TEXT, \
    PRIMARY KEY(reaction_id), \
    FOREIGN KEY (drugbank_id) REFERENCES Drug ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (uniprot_id) REFERENCES UniProt ON DELETE CASCADE ON UPDATE CASCADE, \
    FOREIGN KEY (username,institute) REFERENCES User ON DELETE CASCADE ON UPDATE CASCADE)")"""

"""cur.execute("CREATE TABLE Contributors( \
    reaction_id INTEGER, \
    username TEXT, \
    institute TEXT, \
    PRIMARY KEY (reaction_id, username), \
    FOREIGN KEY (reaction_id) REFERENCES Bindings ON DELETE CASCADE ON UPDATE CASCADE) \
    FOREIGN KEY (username, institute) REFERENCES User ON DELETE CASCADE ON UPDATE CASCADE")"""

"""cur.execute("CREATE TABLE DrugChemicalNotations( \
    drugbank_id TEXT, \
    smiles TEXT, \
    PRIMARY KEY (drugbank_id), \
    UNIQUE(smiles), \
    FOREIGN KEY (drugbank_id) REFERENCES Drug ON DELETE CASCADE ON UPDATE CASCADE)")"""

# To do 1: Add the triggers
# To do 2: Enforce the constraint that the DatabaseManager table can have at most 5 entries

cur.execute("DELETE FROM User")
con.commit()