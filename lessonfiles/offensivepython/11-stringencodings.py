#!/usr/bin/python

def main():
    sample_number = 65

    # We can get binary representations for a number
    print bin(sample_number)  # Results in 0b1000001

    # We can also get hex representations for a number:
    print hex(sample_number)  # Results in 0x41

    # Also, octal:
    print oct(sample_number)  # Results in 0101

    sample_text = "ABCD"

    # Often, we want to convert a string into hex for reason that will be more
    # apparent as you progress further up in CTFs

    print sample_text.encode("hex")  # Results in 41424344

    # Conversely, we can also decode from a hex string

    print "41424344".decode("hex")  # Results in ABCD

    # There are other useful codecs as well:

    print "SGVsbG8=".decode("base64")  # Results in Hello
    print "Obawbhe".decode("rot13")  # Results in Bonjour


if __name__ == "__main__":
    main()
