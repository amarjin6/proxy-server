import signal  # Module provides mechanisms for using signal handlers
import socket
import sys
import threading
import re  # RegEx

config = {
    'HOST': '0.0.0.0',
    'PORT': 8000,
    'MAX_LEN': 65535,
    'TIMEOUT': 50,
    'MEMBERS_AMOUNT': 10,
    'BLACKLIST': ['silvertranscendentoldsunset.neverssl.com', 'https']
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

        self.linkedSites = []

    def listen(self):
        while True:
            # Establish the connection
            (conn, addr) = self.sock.accept()
            t = threading.Thread(name=addr[0], target=self.redirect,
                                 args=(conn,), daemon=True)
            t.start()

    def redirect(self, conn):
        # Get the request from browser
        request = conn.recv(config['MAX_LEN'])

        # Parse the first line
        firstLine = request.decode('utf-8').split('\n')[0]

        # Get url
        try:
            url = firstLine.split(' ')[1]
        except IndexError:
            url = ''

        # Check if the host:port is blacklisted
        for i in range(0, len(config['BLACKLIST'])):
            if config['BLACKLIST'][i] in url:
                print('[!] BLOCKED')
                sys.exit(0)

        httpPos = url.find('://')  # find pos of ://
        if httpPos == -1:
            temp = url
        else:
            temp = url[(httpPos + 3):]  # get the rest of url

        portPos = temp.find(':')  # find the port pos (if any)

        # Find end of web server
        webserverPos = temp.find('/')
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

        # Get IP by hostname
        webserver = socket.gethostbyname(webserver)

        # Сonvert generic message format of RFC 822
        buf1 = re.findall(b'\:\d+\/(.*\s)', request)
        tmp1 = b''.join(buf1)
        reg1 = b'/' + tmp1

        buf2 = re.findall(b'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?',
                          request)
        tmp = []
        for i in range(len(buf2)):
            for j in range(len(buf2[i])):
                tmp.append(buf2[i][j])

        if tmp:
            tmp[0] += b'://'

        reg2 = b''.join(tmp)

        request = request.replace(reg2, reg1)
        reg2 = b''
        reg1 = b''
        request = request.replace(b'http://live.legendy.by:8000/legendyfm', b'/legendyfm')

        # Set up a new connection to the destination server
        try:
            # Create a socket to connect to the web server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(config['TIMEOUT'])
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', port))
            s.connect((webserver, port))
            s.sendall(request)

            # Redirect the server’s response to the client
            while True:
                # receive data from web server
                data = s.recv(config['MAX_LEN'])

                if data:
                    conn.send(data)  # send to browser/client
                    if b'HTTP/' in data and url not in self.linkedSites:
                        self.linkedSites.append(url)
                        answer = data[9:15].decode('utf-8')
                        print(f'{url} - {answer}')
                else:
                    break

        except socket.error as e:
            if s:
                s.close()
            elif conn:
                conn.close()

    def shutdown(self):
        self.sock.close()
        sys.exit(0)


if __name__ == '__main__':
    print('Server is running...')
    server = Proxy()
    server.listen()
