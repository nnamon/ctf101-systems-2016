#! /usr/bin/python

import sys

def write(data):
    sys.stdout.write(data)
    sys.stdout.flush()

def main():
    write("SuperCalculator (e.g. 2+2): ")
    eqn = sys.stdin.readline().strip()
    answer = eval(eqn)
    write("%s = %s\n" % (eqn, answer))

if __name__ == "__main__":
    main()
