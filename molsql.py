import sqlite3
import os
from MolDisplay import Atom, Bond, Molecule
import MolDisplay




class Database:
    def __init__(self, reset=False):
        if reset:
            # delete the database file if it exists
            try:
                os.remove("molecules.db")
            except FileNotFoundError:
                pass
        
        # create a connection to the database file or create a new one
        self.conn = sqlite3.connect("molecules.db")

    def create_tables(self):
        # create a connection to a new or existing database

        # create a cursor object to interact with the database
        c = self.conn.cursor()

        # create Elements table
        c.execute('''CREATE TABLE IF NOT EXISTS Elements
                    (ELEMENT_NO INTEGER NOT NULL,
                    ELEMENT_CODE VARCHAR(3) PRIMARY KEY NOT NULL,
                    ELEMENT_NAME VARCHAR(32) NOT NULL,
                    COLOUR1 CHAR(6) NOT NULL,
                    COLOUR2 CHAR(6) NOT NULL,
                    COLOUR3 CHAR(6) NOT NULL,
                    RADIUS DECIMAL(3) NOT NULL);''')

        # create Atoms table
        c.execute('''CREATE TABLE IF NOT EXISTS Atoms
                    (ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    ELEMENT_CODE VARCHAR(3) NOT NULL,
                    X DECIMAL(7,4) NOT NULL,
                    Y DECIMAL(7,4) NOT NULL,
                    Z DECIMAL(7,4) NOT NULL,
                    FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE));''')

        # create Bonds table
        c.execute('''CREATE TABLE IF NOT EXISTS Bonds
                    (BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    A1 INTEGER NOT NULL,
                    A2 INTEGER NOT NULL,
                    EPAIRS INTEGER NOT NULL);''')

        # create Molecules table
        c.execute('''CREATE TABLE IF NOT EXISTS Molecules
                    (MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    NAME TEXT UNIQUE NOT NULL);''')

        # create MoleculeAtom table
        c.execute('''CREATE TABLE IF NOT EXISTS MoleculeAtom
                    (MOLECULE_ID INTEGER NOT NULL,
                    ATOM_ID INTEGER NOT NULL,
                    PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                    FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID));''')

        # create MoleculeBond table
        c.execute('''CREATE TABLE IF NOT EXISTS MoleculeBond
                    (MOLECULE_ID INTEGER NOT NULL,
                    BOND_ID INTEGER NOT NULL,
                    PRIMARY KEY (MOLECULE_ID, BOND_ID),
                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                    FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID));''')

        # commit changes to the database and close the connection
        self.conn.commit()
        c.close()
        
            
    def __setitem__(self, table, values):
        c = self.conn.cursor()
        placeholders = ", ".join(["?" for i in values])
        c.execute(f"INSERT INTO {table} VALUES ({placeholders})", values)
        self.conn.commit()
        c.close()

    def add_atom(self, molname, atom):
        with self.conn:
            c = self.conn.cursor()

            # add the atom to the Atoms table
            element_code = atom.element
            x, y, z = atom.x,atom.y,atom.z
            c.execute("INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z) VALUES (?, ?, ?, ?)", (element_code, x, y, z))
            atom_id = c.lastrowid

            # add the atom to the MoleculeAtom table
            c.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME=?", (molname,))
            molecule_id = c.fetchone()[0]
            c.execute("INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES (?, ?)", (molecule_id, atom_id))

    def add_bond(self, molname, bond):
        with self.conn:
            c = self.conn.cursor()

            # add the bond to the Bonds table
            a1, a2, epairs = bond.a1,bond.a2,bond.epairs
            c.execute("INSERT INTO Bonds (A1, A2, EPAIRS) VALUES (?, ?, ?)", (a1, a2, epairs))
            bond_id = c.lastrowid

            # add the bond to the MoleculeBond table
            c.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME=?", (molname,))
            molecule_id = c.fetchone()[0]
            c.execute("INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES (?, ?)", (molecule_id, bond_id))


    def add_molecule(self, name, fp):
        with self.conn:
            c = self.conn.cursor()

            # create a MolDisplay.Molecule object and parse the file
            molecule = Molecule()
            molecule.parse(fp)

            # add the molecule to the Molecules table
            c.execute("INSERT INTO Molecules (NAME) VALUES (?)", (name,))
            molecule_id = c.lastrowid

            # add the atoms and bonds to the database
            for i in range(molecule.atom_no):
                atom = molecule.get_atom(i)
                self.add_atom(name, atom)
            for i in range(molecule.bond_no):
                bond = molecule.get_bond(i)
                self.add_bond(name, bond)


    def radius(self):
        query = "SELECT ELEMENT_CODE, RADIUS FROM Elements"
        c = self.conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        c.close()
        return dict(rows)

    def element_name(self):
        query = "SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements"
        c = self.conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        c.close()
        return dict(rows)


    def radial_gradients(self):
        radialGradientSVG = """
        <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
        <stop offset="0%%" stop-color="#%s"/> <stop offset="50%%" stop-color="#%s"/> <stop offset="100%%" stop-color="#%s"/>
        </radialGradient>"""
        query = "SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements"
        results = self.conn.execute(query).fetchall()
        gradients = ""
        for result in results:
            gradients += radialGradientSVG % result
        return gradients



    def load_mol(self, name):
        query = f"""SELECT Atoms.ATOM_ID, ELEMENT_CODE, X, Y, Z
                    FROM Atoms
                    JOIN MoleculeAtom ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
                    JOIN Molecules ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
                    WHERE Molecules.NAME = '{name}'
                    """
        atoms = self.conn.execute(query).fetchall()

        query = f"""SELECT Bonds.BOND_ID, A1, A2, EPairs
                    FROM Bonds
                    JOIN MoleculeBond ON Bonds.BOND_ID = MoleculeBond.BOND_ID
                    JOIN Molecules ON MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
                    WHERE Molecules.NAME = '{name}'
                    """
        bonds = self.conn.execute(query).fetchall()

        mol = Molecule()
        for atom in atoms:
            mol.append_atom(atom[1], atom[2], atom[3], atom[4])
        for bond in bonds:
            mol.append_bond(bond[1], bond[2], bond[3])
        return mol

    def get_molecules(self):
        c = self.conn.cursor()
        c.execute('SELECT NAME FROM Molecules')
        molecules = [row[0] for row in c.fetchall()]
        c.close()
        return molecules
    
    def get_elements(self):
        c = self.conn.cursor()
        c.execute('SELECT ELEMENT_CODE FROM Elements')
        elements = [row[0] for row in c.fetchall()]
        c.close()
        return elements
    
    def delete_elements(self, name):
        c = self.conn.cursor()
        c.execute(f"""DELETE FROM ELEMENTS WHERE ELEMENT_CODE = '{name}'""")
        self.conn.commit()
        c.close()
        return True



if __name__ == "__main__":
    db = Database(reset=True); 
    db.create_tables()

    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 )
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 )
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 )
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 )

    fp = open( 'water-3D-structure-CT1000292221.sdf' ) 
    db.add_molecule( 'Water', fp )

    fp = open( 'caffeine-3D-structure-CT1001987571.sdf' )
    db.add_molecule( 'Caffeine', fp )

    fp = open( 'CID_31260.sdf' )
    db.add_molecule( 'Isopentanol', fp )

    # display tables
    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )
    print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() )
    print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() )
    print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() )
    print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() )
    print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() )
        

    
if __name__ == "__main__":
    db = Database(reset=False); # or use default

if __name__ == "__main__":
    db = Database(reset=False); # or use default
    MolDisplay.radius = db.radius()
    MolDisplay.element_name = db.element_name()
    MolDisplay.header += db.radial_gradients()
    for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
        mol = db.load_mol( molecule )
        mol.sort()
        fp = open( molecule + ".svg", "w" )
        fp.write( mol.svg() )
        fp.close()