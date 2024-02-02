from http.server import HTTPServer, BaseHTTPRequestHandler;

import sys;     # to get command line argument for port
import urllib;  # code to parse for data

import molsql;
import MolDisplay

# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = [ '/index.html', '/style.css', '/script.js' ];

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):

        # used to GET a file from the list ov public_files, above
        if self.path in public_files:   # make sure it's a valid file
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read();
            fp.close();

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) );

        else:
            # if the requested URL is not one of the public_files
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );



    def do_POST(self):

        if self.path == "/sdf_upload.html":
            # code to handle sdf_upload

            molecule = MolDisplay.Molecule();
            for i in range(0,4):    # skip 4 lines
                string = next(self.rfile);

            molsql.add_molecule( self.rfile );

            message = "sdf file uploaded to database";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );

        elif self.path == "/form_handler.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            print( postvars );

            message = "data received";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );




httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
httpd.serve_forever();
