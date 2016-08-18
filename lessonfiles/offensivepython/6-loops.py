#!/usr/bin/python

import random

def main():
    # range() produces a list of numbers
    print range(10)
    # should produce [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # We use this in for loops to create our indexed for loops
    for i in range(10):
        print "This number is", i

    # If you have not already realised the for loop is actually a for-each loop
    travellers = ["Morty", "Rick", "Summer"]
    for i in travellers:
        if i is not "Summer":
            print i, ", you are are allowed to travel in time."
        else:
            print "Go away, Summer."

    # There are also while loops
    counter = 0
    while counter < 10:
        counter += random.randint(0, 5)  # Add a random integer to the counter
        print counter

    # Do while loops do not exist but can be approximated
    while True:
        counter = counter - 1
        if counter < 0:
            print "Stopped!"
            break

if __name__ == "__main__":
    main()
