#!/usr/bin/python

def main():
    # if else conditionals are extremely important
    if True:
        # This definitely gets printed.
        print "I passed"
    else:
        # This never gets printed.
        print "I failed"

    current_year = 2016

    # Conditionals over variables
    if current_year > 2020:
        print "It's the future!"
    elif current_year == 2016:
        print "Come on, it's the CURRENT_YEAR!"
    else:
        print "Absolutely stone age"

    # This is not extremely important but demonstrates conditionals in list
    # comprehensions
    multiples_of_two = [i for i in range(16) if i % 2 == 0]
    print multiples_of_two


if __name__ == "__main__":
    main()
