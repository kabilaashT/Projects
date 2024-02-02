import molecule;
import math;

radius = { 'H': 25,
           'C': 40,
           'O': 40,
           'N': 40,
}

element_name = { 'H': 'grey', 
                 'C': 'black',
                 'O': 'red',
                 'N': 'blue',
               }

header = """<svg version="1.1" width="1000" height="1000" 
                    xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500
offsety = 500


class Atom:
    def __init__(self, c_atom):
        self.c_atom = c_atom
        self.z = c_atom.z
        
    def __str__(self):
        return f"Element: {self.c_atom.element}, x: {self.c_atom.x}, y: {self.c_atom.y}, z: {self.z}"
        
    def svg(self):
        element = self.c_atom.element
        x = self.c_atom.x * 100.0 + offsetx
        y = self.c_atom.y * 100.0 + offsety
        r = radius[element]
        color = element_name[element]
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (x,y,r,color)


# The Bond class represents a chemical bond between two atoms.
class Bond:
    def __init__(self, bond: molecule.bond):  
        # Initialize the Bond object with the given molecule bond.
        self.bond = bond
        self.z = bond.z
    
    def __str__(self):
         # Return a string representation of the bond object.
        return f"Bond: {self.bond.a1}-{self.bond.a2}"
    
    def svg(self):
         # Generate an SVG representation of the bond object.
        x1 = self.bond.x1 * 100.0 + offsetx
        y1 = self.bond.y1 * 100.0 + offsety
        x2 = self.bond.x2 * 100.0 + offsetx
        y2 = self.bond.y2 * 100.0 + offsety
        dx = x2 - x1
        dy = y2 - y1
        d = (dx**2 + dy**2)**0.5
        ux = dx / d
        uy = dy / d
        bx = uy * 10
        by = -ux * 10
        points = [
            (x1 + bx, y1 + by),
            (x1 - bx, y1 - by),
            (x2 - bx, y2 - by),
            (x2 + bx, y2 + by)
        ]
        return ' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (
         # Format the SVG polygon points and return the result
            points[0][0], points[0][1],
            points[1][0], points[1][1],
            points[2][0], points[2][1],
            points[3][0], points[3][1]
        )
class Molecule(molecule.molecule):
    def __str__(self):
        # Create a string representation of the molecule
        s = "Atoms:\n"
        for atom in self.atoms:
            s += f"{atom}\n"
        s += "Bonds:\n"
        for bond in self.bonds:
            s += f"{bond}\n"
        return s
    

    def svg(self):
         # Create SVG string for the molecule
        atoms = []
        for i in range(self.atom_no):
            atoms.append(Atom(self.get_atom(i)))
        bonds = []
        for i in range(self.bond_no):
            bonds.append(Bond(self.get_bond(i)))
        atoms_sorted = sorted(atoms, key=lambda a: a.z)
        bonds_sorted = sorted(bonds, key=lambda b: b.z)
        svg_str = header
          # Merge atoms and bonds into a single SVG string
        a_idx, b_idx = 0, 0
        while a_idx < len(atoms_sorted) and b_idx < len(bonds_sorted):
            atom = atoms_sorted[a_idx]
            bond = bonds_sorted[b_idx]
            if atom.z < bond.z:
                svg_str += atom.svg()
                a_idx += 1
            else:
                svg_str += bond.svg()
                b_idx += 1
        while a_idx < len(atoms_sorted):
            svg_str += atoms_sorted[a_idx].svg()
            a_idx += 1
        while b_idx < len(bonds_sorted):
            svg_str += bonds_sorted[b_idx].svg()
            b_idx += 1
        svg_str += footer
        return svg_str

    def parse(self,f):
        # Skip the first three lines
        f.readline()
        f.readline()
        f.readline()

        # Parse the line that specifies the number of atoms and bonds
        line = f.readline().strip().decode('utf-8').split()
        print(line)
        # mol = molecule.molecule()

        # Parse the atom lines and add them to the molecule
        for i in range(int(line[0])):
            aline = f.readline().strip().decode('utf-8').split()
            self.append_atom(aline[3], float(aline[0]), float(aline[1]), float(aline[2]))

        # Parse the bond lines and add them to the molecule
        for i in range(int(line[1])):
            bline = f.readline().strip().decode('utf-8').split()
            self.append_bond(int(bline[0]) - 1, int(bline[1]) - 1, int(bline[2]))
    
# def parse(f):
# # Skip the first three lines
#     f.readline()
#     f.readline()
#     f.readline()

#     # Parse the line that specifies the number of atoms and bonds
#     line = str(f.readline().strip()).split()
#     print(line)
#     mol = molecule.molecule()

#     # Parse the atom lines and add them to the molecule
#     for i in range(int(line[0])):
#         aline = f.readline().strip().split()
#         mol.append_atom(aline[3],float(aline[0]), float(aline[1]),float(aline[2]))
    
#      # Parse the bond lines and add them to the molecule
#     for i in range(int(line[1])):
#         bline = f.readline().strip().split()
#         mol.append_bond(int(bline[0])-1, int(bline[1])-1, int(bline[2]))
        
#     return mol

    
def sort_atoms(atoms):
# Sort the atoms by atomic symbol, then by x-coordinate, then by y-coordinate, then by z-coordinate
    sorted_atoms = sorted(atoms, key=lambda atom: (atom[3], atom[1], atom[2], atom[3]))
    return sorted_atoms 