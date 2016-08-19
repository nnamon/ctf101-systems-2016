#!/usr/bin/python

def main():
    # Let's create a file
    towrite = open("my_file", "w")  # 'w' stands for open for write

    # Now, we can write a string into it
    towrite.write("some string")

    # Close the file
    towrite.close()

    # We can do the converse option by reading the file
    toread = open("my_file")  # implicitly open for read

    # Read the contents
    contents = toread.read()
    print contents

    # Close the file
    toread.close()

if __name__ == "__main__":
    main()
