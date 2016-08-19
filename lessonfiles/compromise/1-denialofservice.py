#!/usr/bin/python

import socket

def main():
    HOST, PORT = "localhost", 0

    # Create the server, binding to localhost on a free port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)

    # Print the connection information
    print "Please connect to %s %d" % (HOST, server.getsockname()[1])

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    while True:
        # Accept a connection
        conn, addr = server.accept()

        # Interact with the client
        conn.sendall("Please enter the number you wish to square: ")

        # Get the integer
        data = conn.recv(1024)
        number = int(data)

        # Square it
        square = number * number

        # Print the number back to the client as a string
        conn.sendall(str(square) + "\n")

        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
