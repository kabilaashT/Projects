import http.server
import json
import socketserver
import os
from MolDisplay import Molecule
import MolDisplay
import io
from molsql import Database
import cgi

PORT = int(os.environ.get('PORT', 53482))#3482 the last 4 digits are from my student number

db = Database(reset=False)
MolDisplay.radius = db.radius()
MolDisplay.element_name = db.element_name()
MolDisplay.header += db.radial_gradients()
class MyHandler(http.server.BaseHTTPRequestHandler):


    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-length', len(home_page))           
            self.end_headers()

            self.wfile.write (bytes(home_page, 'utf-8'))

        elif (self.path == '/addRemove.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-length', len(add_remove))           
            self.end_headers()

            self.wfile.write (bytes(add_remove, 'utf-8'))

        elif (self.path == '/upload.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-length', len(upload))           
            self.end_headers()

            self.wfile.write (bytes(upload, 'utf-8'))            

        elif (self.path == '/selectMolecule.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-length', len(select))           
            self.end_headers()

            self.wfile.write (bytes(select, 'utf-8'))

        elif(self.path == '/style.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.send_header('Content-length', len(style))           
            self.end_headers()

            self.wfile.write (bytes(style, 'utf-8'))
        
        elif self.path == '/script.js':
            # reaf the file
            # send it to the client... refer to / and /style.css 
            pass
        elif self.path == '/elements':
            # get all the elements from the database
            # return them as a string or json file depending on your preferences
            pass
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/molecule':

            self.rfile.readline()
            self.rfile.readline()
            self.rfile.readline()
            self.rfile.readline()

            molecule_object = MolDisplay.Molecule()
            molecule_object.parse(io.TextIOWrapper(self.rfile))
            molecule_object.sort()
            svg = Molecule(molecule_object).svg()
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()
            self.wfile.write(svg.encode())

        elif self.path == "/add":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = json.loads(post_data)
            
            # Replace this with your database logic
            print(form_data)
            db['Elements'] = (
                form_data['element-number'],
                form_data['element-code'],
                form_data['element-name'],
                form_data['element-colors-1'],
                form_data['element-colors-2'],
                form_data['element-colors-3'],
                form_data['element-radius']
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(b'Data received successfully.')
#remove
        # elif self.path == "/remove":
        #             content_length = int(self.headers['Content-Length'])
        #             raw_post_data = self.rfile.read(content_length)
        #             post_data = json.loads(raw_post_data)
                    
        #             # Assuming you have a dictionary called db to store the elements
        #             db = {}
        #             db['Elements'] = (
        #                 int(post_data['element-number']),
        #                 post_data['element-code'],
        #                 post_data['element-name'],
        #                 form_data['element-colors-1'],
        #                 form_data['element-colors-2'],
        #                 form_data['element-colors-3'],
        #                 float(post_data['element-radius'])
        #             )

        #             self.send_response(200)
        #             self.send_header("Content-type", "application/json")
        #             self.end_headers()
        #             response = {"status": "success"}
        #             self.wfile.write(json.dumps(response).encode())

        elif self.path == "/upload":
            content_type, pdict = cgi.parse_header(self.headers.get("content-type"))
            if content_type == "multipart/form-data":
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                form_data = cgi.parse_multipart(self.rfile, pdict)
                molecule_name = form_data["moleculeName"][0]
                file_data = form_data["filename"][0]
                file_stream = io.BytesIO(file_data)
                db.add_molecule(molecule_name, file_stream)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            response = {"status": "success"}
            self.wfile.write(json.dumps(response).encode())

        # elif self.path == "/select":
        #     content_length = int(self.headers['Content-Length'])
        #     raw_post_data = self.rfile.read(content_length)
        #     post_data = json.loads(raw_post_data)
        #     molecule_name = post_data['molecule-name']

        #     # Assuming the molecule's file is named as the molecule_name
        #     with open(molecule_name, 'rb') as f:
        #         self.parse(f)

        #     svg_data = self.svg()

        #     self.send_response(200)
        #     self.send_header("Content-type", "application/json")
        #     self.end_headers()
        #     response = {"svg": svg_data}
        #     self.wfile.write(json.dumps(response).encode())

        elif self.path == "/selectElement":
            # Assuming you have a function to get the list of molecule names
            # molecule_names = get_molecule_names()
            element_names = db.get_elements()
            print (element_names)
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"elements": element_names}
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == "/deleteElement":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = json.loads(post_data)

            

            name = form_data["element_name"]
            db.delete_elements(name)

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"molecules": 1}
            self.wfile.write(json.dumps(response).encode())


        elif self.path == "/select":
            # Assuming you have a function to get the list of molecule names
            # molecule_names = get_molecule_names()
            molecule_names = db.get_molecules()
            print (molecule_names)
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"molecules": molecule_names}
            self.wfile.write(json.dumps(response).encode())

            # def get_molecule_names(self):
            #     # Implement this function to return the list of molecule names
            #     pass

        elif self.path == "/display":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = json.loads(post_data)

            

            mol = db.load_mol(form_data["mol_name"])
            rotation = form_data["rotation"]

            

            if(rotation=="x"):
                mx = MolDisplay.molecule.mx_wrapper(90,0,0)
                mol.xform( mx.xform_matrix )
            elif(rotation=="y"):
                mx = MolDisplay.molecule.mx_wrapper(0,90,0)
                mol.xform( mx.xform_matrix )
            elif(rotation=="z"):
                mx = MolDisplay.molecule.mx_wrapper(0,0,90)
                mol.xform( mx.xform_matrix )

            svg_data = mol.svg()

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"svg": svg_data}
            self.wfile.write(json.dumps(response).encode())

        elif self.path == '/molecules':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    sql = MolSQL('molecules.db')
                    molecules = sql.get_molecules()
                    response = {'molecules': molecules}
                    self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()


        # else:
        #     self.send_error(404)

        

home_page = open("index.html", "r");
home_page = home_page.read()

add_remove = open("addRemove.html", "r");
add_remove = add_remove.read()

upload = open("upload.html", "r");
upload = upload.read()

select = open("selectMolecule.html", "r");
select = select.read()

style = open("style.css", "r")
style = style.read()


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
