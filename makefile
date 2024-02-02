CC=clang
CFLAGS=-c -g -Wall -pedantic -std=c99
LIBS=-lm # note: the l means library, m means math

all: libmol.so molecule_wrap.o _molecule.so

main: main.o mol.o
	$(CC) main.o mol.o -o main $(LIBS)

main.o: main.c
	$(CC) $(CFLAGS) main.c

mol.o: mol.c mol.h
	$(CC) -fPIC $(CFLAGS) mol.c -o mol.o

libmol.so: mol.o 
	$(CC) -shared mol.o -o libmol.so 

molecule_wrap.o: molecule_wrap.c 
	$(CC) -fPIC $(CFLAGS) -I/Library/Frameworks/Python.framework/Versions/3.10/include/python3.10 molecule_wrap.c -o molecule_wrap.o

_molecule.so: molecule_wrap.o libmol.so
	$(CC) -shared -dynamiclib molecule_wrap.o -L. -L/Library/Frameworks/Python.framework/Versions/3.10/lib -lmol -lpython3.10 -o _molecule.so


# molecule_wrap.o: molecule_wrap.c 
# 	$(CC) -fPIC $(CFLAGS) -I/usr/include/python3.7m molecule_wrap.c -o molecule_wrap.o

# _molecule.so: molecule_wrap.o libmol.so
# 	$(CC) -shared -dynamiclib molecule_wrap.o -L. -L/usr/11b/python3.7/config-3.7m-x86_64-linux-gnu -lmol -lpython3.7m -o _molecule.so

clean:
	rm -f *.*o main
