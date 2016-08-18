#!/usr/bin/python

def main():
    users = "admin:passwd chrome:metal emacs:vims"

    # We can do string splits by spaces
    users_split = users.split()

    print users_split
    # Result is ['admin:passwd', 'chrome:metal', 'emacs:vims']

    # We can also split strings by an arbitrary string sequence
    for i in users_split:
        creds_split = i.split(":")
        print "Username:", creds_split[0], "Password:", creds_split[1]

    # Get only the usernames
    usernames = [i.split(":")[0] for i in users_split]

    # Join the usernames with a comma
    commaed = ", ".join(usernames)

    print commaed  # Results in admin, chrome, emacs

    # I cannot speel
    cantspell = "Faaling, Paaling, Faat, Graat, Laaks"

    # You can replace substrings within strings
    canspell = cantspell.replace("aa", "ee")

    print canspell  # Results in Feeling, Peeling, Feet, Greet, Leeks

    # You can call methods directly on strings as well
    print "shout".upper()  # Results in SHOUT

if __name__ == "__main__":
    main()
