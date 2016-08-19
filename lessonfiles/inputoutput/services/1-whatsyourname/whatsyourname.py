#!/usr/bin/python

import sys

flag = file("/home/whatsyourname/flag").read()

def write(contents, term="\n"):
    sys.stdout.write(contents + term)
    sys.stdout.flush()

def main():
    write("What is your name? ", term="")
    name = sys.stdin.readline().strip()
    write("Welcome %s, here's your flag: %s" % (name, flag), term="")

if __name__ == '__main__':
    main()

