import http.server
from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi

PORT_NUMBER = 8080

#This class will handle anyincoming requests from the browser 

class myHandler(BaseHTTPRequestHandler):
        #handler for the Get requests
        def do_GET(self):
            if self.path=="/":
                self.path="/index_example4.html"

            try:
                #Check the file extension required and set the right mime type

                sendReply = False
                if self.path.endswith(".html"):
                    mimetype='text/html'
                    sendReply = True
                if self.path.endswith(".jpg"):
                    mimetype='image/jpg'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype='image/gif'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype='application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype='text/css'
                    sendReply = True

                if sendReply == True:
                    #open the static file requested and send it
                    f = open(curdir + sep + self.path)
                    self.send_response(200)
                    self.send_header('Content-type' ,mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                return 

            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)

    #Handler for the POST requests
def do_POST(self):
    if self.path=="/send":
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD' : 'POST', 
                        'CONTENT_TYPE':self.headers['Content-Type'],
        })

        print("Your name is: %s" % form["your_name"].value)
        self.send_response(200)
        self.endheaders()
        self.wfile.write("Thanks %s !" % form["firstname"].value %" " %form["lastname"])
        return
 
try:
    #Create a web server and define the handler to manage the incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    #wait forever for incomping htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()