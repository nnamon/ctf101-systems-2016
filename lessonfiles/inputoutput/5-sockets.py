#!/usr/bin/python

import socket

def main():
    # Create a socket
    sock = socket.socket()

    # Connect the socket to the remote service
    sock.connect(("pwn.spro.ink", 1337))

    # Receive the first prompt
    prompt = sock.recv(1024)  # Receive an arbitrary max 1024 bytes
    print prompt

    # Send our name
    sock.send("Elliot Alderson\n")  # Remember the newline at the end

    # Receive the flag
    flagline = sock.recv(1024)

    print flagline

if __name__ == "__main__":
    main()
