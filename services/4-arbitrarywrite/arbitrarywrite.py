#! /usr/bin/python

import sys

# global variables
logged_in = False
admin = False
FLAG = open("/home/arbitrarywrite/flag").read()

def write(data):
    sys.stdout.write(data)
    sys.stdout.flush()

def main():
    write("Secret Storage 1.0\n")
    while True:
        if not logged_in:
            # Print the menu
            write("You are not logged in. Please choose one option: \n")
            write("1. Log in\n")
            write("2. Create Account\n")

            # Read the choice
            choice = sys.stdin.readline().strip()

            # Read the username and password
            write("Please enter your name: ")
            name = sys.stdin.readline().strip()
            write("Please enter your password: ")
            password = sys.stdin.readline().strip()

            # Process the choices
            if choice == "1":
                if validate(name, password):
                    write("Success!\n")
                else:
                    write("Failure!\n")
            elif choice == "2":
                create_user(name, password)
            else:
                write("Invalid choice.\n")

        else:
            # Already logged in
            write("Welcome %s!\n" % logged_in)
            write("1. Retrieve secret\n")
            write("2. Store secret\n")
            write("3. Read admin secret\n")

            # Read the choice from the user
            choice = sys.stdin.readline().strip()

            # Process the choice
            if choice == "1":
                write("Which secret would you like to retrieve: ")
                secretname = sys.stdin.readline().strip()
                retrieve_secret(secretname)
            elif choice == "2":
                write("What is the name of the secret you want to store: ")
                secretname = sys.stdin.readline().strip()
                write("What secret would you like to store: ")
                secret = sys.stdin.readline().strip()
                store_secret(secretname, secret)
            elif choice == "3":
                reveal_secret()
            else:
                write("Invalid choice.\n")

# Retrieve the secrets from the file
def retrieve_secret(secretname):
    if "flag" in secretname:
        write("Privileged secret requires admin writes\n")
        return
    try:
        with open("/home/arbitrarywrite/secrets/%s" % (secretname)) \
            as secretfile:
            write("Here's your secret: %s\n" % secretfile.read())
    except:
        write("No such secret\n")

# Write secrets to file
def store_secret(secretname, secret):
    try:
        with open("/home/arbitrarywrite/secrets/%s" % (secretname), "w") \
            as secretfile:
            secretfile.write(secret)
            write("Secret written!\n")
    except:
        write("Error in writing secret.\n")

# Reveal the secrets if the user is logged in and admin
def reveal_secret():
    if admin:
        write("Here is the admin's secret: %s\n" % FLAG)
    else:
        write("You are not admin.\n")

# Validate the username and password
def validate(name, password):
    try:
        with open("/home/arbitrarywrite/accounts/" + name) as accountfile:
            adminflag, filepassword = accountfile.read().split(":")
            if password == filepassword:
                global logged_in
                logged_in = name
                if adminflag == "1":
                    global admin
                    admin = True
                return True
    except:
        write("No such account.\n")
    return False

# Create users by writing them to file
def create_user(name, password):
    with open("/home/arbitrarywrite/accounts/" + name, "w") as accountfile:
        accountfile.write("0:" + password)
    write("Account created. Please log in.\n")

if __name__ == "__main__":
    main()
