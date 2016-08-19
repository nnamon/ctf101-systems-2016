#!/usr/bin/python

#import the os
import os

def main():
    # We can run shell commands by using os.system('shell command')
    # This is the equivalent of running sh -c '<your command here>' so things
    # like pipes, redirects, semicolons work.

    # /usb/bin/md5sum is the program to execute
    # /etc/issue.net is the first argument to the program
    os.system("/usr/bin/md5sum /etc/issue.net")

    # Let's demonstrate that the features of the shell is available to us.
    os.system("echo 'Hello, Friend' > badfile; cat badfile")

if __name__ == "__main__":
    main()
