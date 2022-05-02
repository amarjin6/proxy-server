import signal  # Module provides mechanisms for using signal handlers
import socket
import sys
import threading

config = {
    'HOST': 'localhost',
    'PORT': 8000,
    'MAX_LEN': 1024,
    'TIMEOUT': 5,
    'MEMBERS_AMOUNT': 10
}


class Proxy:
    def __init__(self):
        # Shutdown on Ctrl+C
        signal.signal(signal.SIGINT, self.shutdown)

        # Create a TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to a public host, and a port
        self.sock.bind((config['HOST'], config['PORT']))

        self.sock.listen(config['MEMBERS_AMOUNT'])  # become a server socket

    def listen(self):
        while True:
            # Establish the connection
            (conn, addr) = self.sock.accept()
            t = threading.Thread(name=addr[0], target=self.redirect,
                                 args=(self, conn, addr), daemon=True)
            t.start()

    @staticmethod
    def redirect(conn, addr):
        # Get the request from browser
        request = conn.recv(config['MAX_LEN'])

        # Parse the first line
        firstLine = request.decode('utf-8').split('\n')[0]

        # Get url
        try:
            url = firstLine.split(' ')[1]
        except IndexError:
            url = ''

        httpPos = url.find("://")  # find pos of ://
        if httpPos == -1:
            temp = url
        else:
            temp = url[(httpPos + 3):]  # get the rest of url

        portPos = temp.find(":")  # find the port pos (if any)

        # Find end of web server
        webserverPos = temp.find("/")
        if webserverPos == -1:
            webserverPos = len(temp)

        if portPos == -1 or webserverPos < portPos:
            # default port
            port = 80
            webserver = temp[:webserverPos]

        else:
            # specific port
            port = int((temp[(portPos + 1):])[:webserverPos - portPos - 1])
            webserver = temp[:portPos]

        # Set up a new connection to the destination server
        try:
            # Create a socket to connect to the web server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(config['TIMEOUT'])
            s.bind((webserver, port))
            s.connect((webserver, port))
            s.sendall(request)

            # Redirect the server’s response to the client
            while 1:
                # receive data from web server
                data = s.recv(config['MAX_LEN'])

                if data:
                    conn.send(data)  # send to browser/client
                else:
                    break

                s.close()
                conn.close()

        except socket.error as e:
            print(f'Failed to set up new connection: {addr} , {e}')
            if s:
                s.close()
            elif conn:
                conn.close()

    def shutdown(self):
        self.sock.close()
        sys.exit(0)


if __name__ == "__main__":
    print('Server is running...')
    server = Proxy()
    server.listen()
