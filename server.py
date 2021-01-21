import socket
import threading


class Server:
    """ Represents a server class. """

    host: str
    port: int
    connections = []
    addresses = []
    usernames = []

    def __init__(self, host, port):
        """
        Constructor.
        :param host: The host name of the server
        :type host: str
        :param port: The port of the server
        :type port: int
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_socket(self):
        """
        Creates a socket.
        :return: None
        """
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen()
            print(f"Server listening on port {self.port}")
        except socket.error:
            print("[Err: Socket creation error]")

    def accept_conn(self):
        """
        Multi threaded method to accept connections.
        :return: None
        """
        try:
            while True:
                conn, address = self.sock.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, address))
                thread.start()
        except socket.error:
            print("[Err: Trouble accepting connection]")
        except KeyboardInterrupt:
            print("Server is shutting down...")

    def handle_client(self, conn, address):
        """
        Threaded method to handle clients individually.
        :param conn: Connection object of the client
        :type conn:
        :param address: Address of the client
        :type address: tuple
        :return: None
        """
        conn.send("Connected to server".encode('utf-8'))
        # Check if username's already taken
        while True:
            username = conn.recv(99).decode('utf-8')
            if username not in self.usernames:
                conn.send('0'.encode('utf-8'))
                break
            conn.send('1'.encode('utf-8'))

        self.connections.append(conn)
        self.addresses.append(address)
        self.usernames.append(username)

        message = f"[{username}] has joined the chat!"
        self.broadcast(message)

        try:
            while True:
                message = f"[{username}] {conn.recv(1024).decode('utf-8')}"
                self.broadcast(message)
        except socket.error:
            print(f"[Err: Lost connection from [{username}] {address[0]}:{address[1]}]")
            # Delete the client entries form the lists
            self.usernames.remove(username)
            self.connections.remove(conn)
            self.addresses.remove(address)
            print(f"Removed {username} from the list")
            self.broadcast(f"[{username} has left the chat!]")

    def broadcast(self, message):
        """
        Broadcast message to all the participants.
        :param message: Message to be distributed to clients
        :type message: str
        :return: None
        """
        # Loop through every clients conn object
        for conn in self.connections:
            conn.send(message.encode('utf-8'))


if __name__ == '__main__':
    # server = Server('127.0.0.1', 55555)
    server = Server('', 55555)
    server.create_socket()
    server.accept_conn()
    server.sock.close()
