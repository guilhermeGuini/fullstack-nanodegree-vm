from http.server import BaseHTTPRequestHandler
import cgi

class hello():

    def doGet(handler: BaseHTTPRequestHandler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()

        output = ""
        output += "<html><body>"
        output += "<h1>Hello!</h1>"
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"
        output += "</body></html>"
        handler.wfile.write(output.encode('utf-8'))
        print(output)
        return

    def doGetHola(handler: BaseHTTPRequestHandler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()

        output = ""
        output += "<html><body>Hola <a href='/hello'>Back to Hello</a>"
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"
        output += "</body></html>"
        handler.wfile.write(output.encode('utf-16'))
        print(output)
        return

    def doPost(handler: BaseHTTPRequestHandler):
        handler.send_response(301)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        ctype, pdict = cgi.parse_header(handler.headers.get('Content-Type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(handler.rfile, pdict)
            messagecontent = fields.get('message')

        output = ""
        output += "<html><body>"
        output += "<h2> Okay, how about this: </h2>"
        output += "<h1> %s </h1>" % messagecontent[0]

        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"

        output += "</body></html>"
        handler.wfile.write(output.encode('utf-8'))
        print(output)
        return