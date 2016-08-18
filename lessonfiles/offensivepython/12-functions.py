#!/usr/bin/python

def alone():
    print "I am alone."

def feed(food):
    print "I am fed", food

def add(a, b):
    return a + b

def main():
    # We can call a function with no parameters
    alone()

    # Or we can call it with a parameter
    feed("tacos")

    # Functions can be nested
    print add(add(1, 2), 3)

if __name__ == "__main__":
    main()
