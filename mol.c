#include "mol.h"


void atomset( atom *atom, char element[3], double *x, double *y, double *z ){    
    //copy element into atom->element
    strcpy(atom->element, element);
    //copy coordinates into atom->x, atom->y, atom->z
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

void atomget( atom *atom, char element[3], double *x, double *y, double *z ){
  // copy the values of the atom to the corresponding locations
  strcpy(element, atom->element);
  *x = atom->x;
  *y = atom->y;
  *z = atom->z;
}

void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs) {
    bond->a1 = *a1;   
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = atoms[*a1];
    
    compute_coords(bond);
}


void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs) {
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}

void compute_coords(bond *bond) {
    atom *atom1 = bond->atoms + bond->a1;
    atom *atom2 = bond->atoms + bond->a2;

    // compute z
    bond->z = (atom1->z + atom2->z) / 2.0;

    // compute x1, y1, x2, y2
    bond->x1 = atom1->x;
    bond->y1 = atom1->y;
    bond->x2 = atom2->x;
    bond->y2 = atom2->y;

    // compute len
    double dx = bond->x2 - bond->x1;
    double dy = bond->y2 - bond->y1;
    bond->len = sqrt(dx * dx + dy * dy);

    // compute dx, dy
    bond->dx = dx / bond->len;
    bond->dy = dy / bond->len;
}


/* molmalloc function creates and allocates memory for a molecular structure */
molecule* molmalloc(unsigned short atom_max, unsigned short bond_max) {
    // allocate memory for the molecule structure
    molecule* mol = (molecule*)malloc(sizeof(molecule));
    if (mol == NULL) { 
        return NULL;  /* if allocation fails, return NULL */
    }
    /* set the maximum number of atoms for the molecule */
    mol->atom_max = atom_max;
    mol->atom_no = 0;
    mol->atoms = (atom *)malloc(sizeof(atom) * atom_max);
    if (mol->atoms == NULL) {
        free(mol);
        return NULL;/* if allocation fails, free the previous memory allocation and return NULL */
    }
    /* allocate memory for the atom pointers in the molecule */ 
    mol->atom_ptrs = (atom**)malloc(sizeof(atom*) * atom_max);
    if (mol->atom_ptrs == NULL) {
        free(mol->atoms);
        free(mol);
        return NULL; /* if allocation fails, free the previous memory allocation and return NULL */
    }
    /* setting the maximum number of bonds for the molecule */
    mol->bond_max = bond_max;
    mol->bond_no = 0;
    mol->bonds = (bond*)malloc(sizeof(bond) * bond_max);
    if (mol->bonds == NULL) {
        free(mol->atom_ptrs);
        free(mol->atoms);
        free(mol);
        return NULL;  /* if allocation fails, free the previous memory allocation and return NULL */
    }
    /* allocate memory for the bond pointers in the molecule */
    mol->bond_ptrs = (bond**)malloc(sizeof(bond*) * bond_max);
    if (mol->bond_ptrs == NULL) {
        free(mol->bonds);
        free(mol->atom_ptrs);
        free(mol->atoms);
        free(mol);
        return NULL;   /* if allocation fails, free the previous memory allocation and return NULL */
    }
    return mol;
}


molecule* molcopy(molecule* src){
    
    molecule* dest = molmalloc(src->atom_max, src->bond_max); //Allocate memory
    dest->atom_no = 0;
    dest->bond_no = 0;
    //Copy content of atoms array
    for(int i = 0; i < src->atom_no; i++){
        molappend_atom(dest,&(src->atoms[i]));
    }
    //Copy content of atom_ptr array
    for(int i = 0; i < src->bond_no; i++){
        molappend_bond(dest,&(src->bonds[i]));
    }
    
    return dest;
}

/* molfree function frees up memory for a molecule */
void molfree(molecule *ptr){
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

/* molappend_atom function adds an atom to a molecule */
void molappend_atom(struct molecule *molecule, struct atom *atom) {
    if (molecule->atom_no == molecule->atom_max) {
        /* If the maximum number of atoms is 0, set it to 1 */
        if (molecule->atom_max == 0) {
            molecule->atom_max = 1;
        } else {
            molecule->atom_max *= 2;  /* If the maximum number of atoms is not 0, double it */
        }
        molecule->atoms = realloc(molecule->atoms, molecule->atom_max * sizeof(struct atom));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, molecule->atom_max * sizeof(struct atom*));
    }
    /* Add the new atom to the end of the atoms array in the molecule */
    molecule->atoms[molecule->atom_no++] = *atom;
    /* Update the atom pointers array in the molecule to point to the new atom */
    for(int i = 0; i < molecule->atom_no;i++){
        molecule->atom_ptrs[i] = &(molecule->atoms[i]);
    }
}
   
/* molappend_bond function adds an bond to a molecule */   
void molappend_bond(molecule *molecule, bond *bond) {
    if (molecule->bond_no == molecule->bond_max) {
        /* If the maximum number of bonds is 0, set it to 1 */
        if (molecule->bond_max == 0) {
            molecule->bond_max = 1;
        } else {
            molecule->bond_max *= 2;  /* If the maximum number of bonds is not 0, double it */
        }
        molecule->bonds = realloc(molecule->bonds, molecule->bond_max * sizeof(struct bond));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, molecule->bond_max * sizeof(struct bond*));
    }
    /* Add the new bond to the end of the bonds array in the molecule */
    molecule->bonds[molecule->bond_no++] = *bond;
    /* Update the bond pointers array in the molecule to point to the new bond */
    for(int i = 0; i < molecule->bond_no;i++){
        molecule->bond_ptrs[i] = &(molecule->bonds[i]);
    }
}

/* atom_cmp function compares two atoms */
int atom_cmp(const void *a, const void *b) {
    atom **aa = (atom **)a;
    atom **bb = (atom **)b;
    if ((*aa)->z < (*bb)->z)
        return -1;
    else if ((*aa)->z > (*bb)->z) 
        return 1;
    else 
        return 0;
}

int bond_comp(const void *a, const void *b)
{
    const bond **aa = (const bond **)a;
    const bond **bb = (const bond **)b;

    return (*aa)->z - (*bb)->z;
}


void molsort(molecule *molecule) {
    // Compare function for sorting atom_ptrs array


    // Sort the atom_ptrs array in place
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom *), atom_cmp);

    // Sort the bond_ptrs array in place
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond *), bond_comp);
}

// This function performs a rotation transformation in the x-axis
void xrotation(xform_matrix xform_matrix, unsigned short deg) {
    double Rad = deg * PI_NUMBER / 180.0;  // Convert degrees to radians
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(Rad);
    xform_matrix[1][2] = -sin(Rad);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(Rad);
    xform_matrix[2][2] = cos(Rad);
}

// This function performs a rotation transformation in the y-axis
void yrotation(xform_matrix xform_matrix, unsigned short deg) {
    double Rad = deg * PI_NUMBER / 180.0;  // Convert degrees to radians
    xform_matrix[0][0] = cos(Rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(Rad);
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin(Rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(Rad);
}


// This function performs a rotation transformation in the z-axis
void zrotation(xform_matrix xform_matrix, unsigned short deg) {
    double Rad = deg * PI_NUMBER / 180.0;  // Convert degrees to radians
    xform_matrix[0][0] = cos(Rad);
    xform_matrix[0][1] = -sin(Rad);
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin(Rad);
    xform_matrix[1][1] = cos(Rad);
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

void apply_matrix(xform_matrix matrix, double *x, double *y, double *z) {
    double x1 = *x;
    double y1 = *y;
    double z1 = *z;
    *x = matrix[0][0] * x1 + matrix[0][1] * y1 + matrix[0][2] * z1;
    *y = matrix[1][0] * x1 + matrix[1][1] * y1 + matrix[1][2] * z1;
    *z = matrix[2][0] * x1 + matrix[2][1] * y1 + matrix[2][2] * z1;
}


void mol_xform(molecule *mol, xform_matrix matrix) {
    for (int i = 0; i < mol->bond_no; i++) {
        bond *b = &(mol->bonds[i]);
        double x1 = b->x1;
        double y1 = b->y1;
        double z1 = b->z;
        double x2 = b->x2;
        double y2 = b->y2;
        double z2 = b->z;
        apply_matrix(matrix, &x1, &y1, &z1);
        apply_matrix(matrix, &x2, &y2, &z2);
        b->x1 = x1;
        b->y1 = y1;
        b->z = z1;
        b->x2 = x2;
        b->y2 = y2;
        b->z = z2;
        compute_coords(b);
    }
}

