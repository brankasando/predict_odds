from http.server import BaseHTTPRequestHandler, HTTPServer

import sqlite3



class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        con = sqlite3.connect('bets.db')
        cur = con.cursor()

        cur.execute(
            '''
            select * from scheduled_games order by id
            '''
        )

        records = cur.fetchall()

        print("Total rows are:  ", len(records))



        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Simple Server</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))

        for index, row in enumerate(records):
            print(index)

            self.wfile.write(bytes(row[5], "utf-8"))
            self.wfile.write(bytes("<br>", "utf-8"))

        cur.close()
        con.close()

        self.wfile.write(bytes("<p>Dembeli rezultati///.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer(('localhost', 8080), MyServer)
    print("Yang's local server started at port 8080")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")