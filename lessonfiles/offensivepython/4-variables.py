#!/usr/bin/python

# Creating a 'global' variable
var_global = 1337

def main():
    # Creating a variable that holds an integer
    var_one = 54321

    # Creating two variables that hold strings
    var_two = "I am a string"
    var_three = 'I too am a string, even though my quotes are single'

    # Creating a list object
    var_four = []

    # Creating a dict object
    var_five = {}

    # Creating a tuple object with two integers
    var_six = (41, 42)

    # Creating a file object from /etc/passwd
    var_seven = open("/etc/passwd")

    # Printing the contents of the file object by referencing a method
    print var_seven.read()



if __name__ == "__main__":
    main()
