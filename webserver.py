from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                resPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = resPath).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s?</h1>" % myRestaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action= '/restaurant/%s/delete'>" % resPath
                output += "<input type ='submit' value = 'Delete'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            
            if self.path.endswith("/edit"):
                resPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = resPath).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>" % myRestaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action= '/restaurant/%s/edit'>" % resPath
                output += "<input name = 'newName' type = 'text' placeholder = '%s'>" % myRestaurantQuery.name
                output += "<input type ='submit' value = 'Rename'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
                
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a new restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action= '/restaurant/new'>"
                output += "<input name = 'newResName' type = 'text' placeholder = 'New Restaurant Name'>" 
                output += "<input type ='submit' value = 'Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
                
            if self.path.endswith("/restaurant"):
                results = session.query(Restaurant).all();
                output = ""
                output += "<a href='/restaurant/new'>Make a new restaurant</a><br><br>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for item in results:
                    output += item.name
                    output += "<br><a href='restaurant/%s/edit'>Edit</a>" % item.id
                    output += "<br><a href='restaurant/%s/delete'>Delete</a>" % item.id
                    output += "<br><br><br>"
 
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:           
            if self.path.endswith("/restaurant/new"):               
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newResName')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newName')
                
                resPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = resPath).one()
                myRestaurantQuery.name = messagecontent[0]
                session.add(myRestaurantQuery)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                
                resPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = resPath).one()
                session.delete(myRestaurantQuery)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

            
        except:
            pass
 
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
