from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from restaurantdataaccess import get_restaurants, create_restaurant, get_restaurant_by_id, update_restaurant, delete_restaurant


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Create a new Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                <input name="newRestaurantName" type="text" ><br><br>
                <input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())

            if self.path.endswith("/edit"):
                id = self.path.split("/")[2]
                restaurant = get_restaurant_by_id(id)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += restaurant.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurant.id
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % restaurant.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output.encode())
                return

            if self.path.endswith("/delete"):
                id = self.path.split("/")[2]
                restaurant = get_restaurant_by_id(id)
                if restaurant:
                    delete_restaurant(restaurant)
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    # self.send_response(200)
                    # self.send_header('Content-type', 'text/html')
                    # self.end_headers()
                    # output = ""
                    # output += "<html><body>"
                    # output += "<h1>Are you sure you want to delete %s?" % restaurant.name
                    # output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurant.id
                    # output += "<input type = 'submit' value = 'Delete'>"
                    # output += "</form>"
                    # output += "</body></html>"
                    # self.wfile.write(output.encode())

            if self.path.endswith("/restaurants"):
                restaurants = get_restaurants()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1 >Restaurants List</h1>"
                output += "<br>"
                output += "<a href='/restaurants/new'>Create a new Restaurant</a> "
                for restaurant in restaurants:
                    print(restaurant.name,restaurant.id)
                    output += "<h2> %s </h2>" % restaurant.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a> " % restaurant.id
                    output += "<a href ='/restaurants/%s/delete'> Delete </a>" % restaurant.id
                    output += "</br>"
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output.encode())
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                message = ""
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('newRestaurantName')
                    message = str(message_content[0]).replace("b'", "")
                    message = message.replace("'", "")

                create_restaurant(message)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('newRestaurantName')
                    message = str(message_content[0]).replace("b'", "")
                    message = message.replace("'", "")
                    id = self.path.split("/")[2]
                    restaurant = get_restaurant_by_id(id)
                    if restaurant:
                        restaurant.name = message
                        update_restaurant(restaurant)
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                id = self.path.split("/")[2]
                restaurant = get_restaurant_by_id(id)
                if restaurant:
                    delete_restaurant(restaurant)
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except Exception as e:
            print(e)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
