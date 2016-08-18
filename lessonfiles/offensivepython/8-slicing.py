#!/usr/bin/python

def main():
    # We create a list of numbers
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Slices let you create sublists from an original list
    # Syntax for slices look like: list[start_including:stop_excluding:step]
    one_to_three = numbers[1:4]  # Remember we exclude the last index

    print one_to_three  # Results in [1, 2, 3]

    # We can also omit arguments to signify either a from start or to end
    zero_to_four = numbers[:5]
    seven_to_nine = numbers[7:]

    print zero_to_four  # Results in [0, 1, 2, 3, 4]
    print seven_to_nine  # Results in [7, 8, 9]

    # We can skip numbers by providing a step
    twos = numbers[::2]
    threes = numbers[::3]

    print twos  # Results in [0, 2, 4, 6, 8]
    print threes # Results in [0, 3, 6, 9]

    # We can also reverse the list
    rev_numbers = numbers[::-1]

    print rev_numbers  # Results in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

if __name__ == "__main__":
    main()
