#!/usr/bin/python

def main():
    # This might look like magic but it is basically a loop within a list
    mults_of_two = [i*2 for i in range(100)]

    # This allows us to create some really useful transformations
    fruits = ["apple", "orange", "mango", "blueberries"]
    fruit_lengths = [len(i) for i in fruits]

    # We can even make it look like an indexed loop
    fruit_output = ["%s (%d)" % (fruits[i], fruit_lengths[i]) for i in
                    range(len(fruits))]

    # Insert newlines in between the fruit outputs and print the entire string
    print "\n".join(fruit_output)

if __name__ == "__main__":
    main()
