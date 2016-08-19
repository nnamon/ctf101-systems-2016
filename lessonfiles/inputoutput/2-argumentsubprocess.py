#!/usr/bin/python

# import the subprocess module
import subprocess

def main():
    # With subprocess, you no longer have a shell environment since the program
    # is called directly instead of your commands being wrapped for execution
    # in a shell. The subprocess.call() function takes a list of strings where
    # the first string is the path to the program to execute and the following
    # strings the arguments to the program.

    # /usb/bin/md5sum is the program to execute
    # /etc/issue.net is the first argument to the program
    subprocess.call(["/usr/bin/md5sum", "/etc/issue.net"])


if __name__ == "__main__":
    main()
