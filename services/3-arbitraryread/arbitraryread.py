#!/usr/bin/python
# I might have left a little present at /flag

import sys

def write(data, term="\n"):
    sys.stdout.write(data + term)
    sys.stdout.flush()

def main():
    # Tell the user what we have
    write("Our selection: futurama, ghost, pinkfloyd, rat")
    write("Take your pick: ", term="")

    # What did they pick
    pick = sys.stdin.readline().strip()

    # Try reading the art
    try:
        location = "/home/arbitraryread/art/" + pick
        contents = open(location).read()
    except:
        write("Unable to read the art from file...")
        exit()

    # Give them the art
    write(contents)

if __name__ == "__main__":
    main()
