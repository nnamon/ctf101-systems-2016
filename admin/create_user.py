#!/usr/bin/python

import subprocess
import pwd
import re
import random
import string
import socket
import md5
import os

def genpass():
    syms = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = "".join(random.choice(syms) for i in range(10))
    return password

def main():
    print "---------------------------------------"
    print "| Welcome to the CTF101 2016 Workshop |"
    print "|   User Account Creation Utility     |"
    print "---------------------------------------"
    print "\n"
    username = raw_input("Enter your desired username: ")

    try:
        user = pwd.getpwnam(username)
        exists = True
    except KeyError:
        exists = False

    if exists:
        print "Sorry that username is already taken."
        exit()

    pat = re.compile("^[a-z]+$")
    mat = pat.match(username)

    if not mat:
        print "Sorry the username is invalid (not matching ^[a-z]+$)"
        exit()

    captcha = "".join(random.choice(string.ascii_letters) for i in range(7))
    os.system("echo %s | toilet --gay" % captcha)

    captcha_user = raw_input("Please solve the captcha: ")

    if captcha_user != captcha:
        print "Captcha is wrong :)"
        exit()

    password = genpass()
    cryptpass = subprocess.check_output(["/usr/bin/openssl",
                                         "passwd", "-1", password]).strip()

    parameters = ["/usr/sbin/useradd", "-s", "/bin/bash", "-m", "-g",
                  "ctfusers", "-p", cryptpass, username]
    subprocess.call(parameters)
    subprocess.call(["/usr/sbin/edquota", "-p", "quotaproto", username])

    hashed = md5.md5(password).hexdigest()

    print "Here are your credentials:"
    print "Username: %s" % username
    print "Password: %s\n" % password

    print "Please login with %s@ssh.spro.ink using the provided password" % username

main()

