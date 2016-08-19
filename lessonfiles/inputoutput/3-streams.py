#!/usr/bin/python

import subprocess

def main():
    # Let's try and emulate echo "hello" | base64

    # We can't use the old method of subprocess.call anymore. We would have to
    # deal a little closer to the metal with subprocess.Popen.

    # Note the way we instantiate the object. We have to let the constructor
    # know that we want to interact with the stdin and stdout streams otherwise
    # it would go to the shell instead of our script.
    process = subprocess.Popen("/usr/bin/base64",
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)

    # We need to write hello into the process' stdin stream
    process.stdin.write("hello")

    # Close the stream to let the program know we're done
    process.stdin.close()

    # We can now retrieve the output from stdout
    output = process.stdout.read()

    # Finally, let's print the output
    print output

if __name__ == "__main__":
    main()
