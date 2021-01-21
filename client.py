import threading
import socket
import sys
import os

# Identify shell command to clear console on *nix/windows
clear = lambda x: os.system('cls') if x == 'win32' else os.system('clear')


class Client:
    """ Represents a client class. """

    HOST = '127.0.0.1'
    PORT = 55555
    try_count = 4

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def provide_username(self):
        """
        Method to authenticate i.e login/register.
        :return: None
        """
        # Check if username's already taken
        while True:
            username = input('username: ')
            self.sock.send(username.encode('utf-8'))
            if self.sock.recv(2).decode('utf-8') == '0':
                break
            print("Username already taken")

    def send_message(self):
        """
        Send messages to the server.
        :return: None
        """
        try:
            while True:
                self.sock.send(input().encode('utf-8'))
        except socket.error:
            print("Cannot send messages")

    def receive_message(self):
        """
        Receive messages from the server.
        :return: None
        """
        try:
            while True:
                message = self.sock.recv(1024).decode('utf-8')
                print(f"{message}")
        except socket.error:
            print("Messages could not be retrieved")

    def run(self):
        """
        Method entry point to create socket and connect to the server.
        :return: None
        """
        try:
            # TODO: Try using bind()
            self.sock.connect((self.HOST, self.PORT))
            print(self.sock.recv(1024).decode('utf-8'))
            self.provide_username()

            # Create threads for send_message() and receive_message() methods
            thread_send = threading.Thread(target=self.send_message)
            thread_recv = threading.Thread(target=self.receive_message)
            thread_send.start()
            thread_recv.start()
        except socket.error:
            # Try connecting 4 times to the server
            while self.try_count > 0:
                clear(sys.platform)
                print("Trying to reach the server...")
                self.try_count -= 1
                self.run()

            clear(sys.platform)
            print("Server is currently unavailable :(")


if __name__ == '__main__':
    app = Client()
    app.run()
    # app.sock.close()
