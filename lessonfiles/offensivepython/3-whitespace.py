#!/usr/bin/python

# This runs at the global scope.
alpha = 1

def main():
    # This runs at the scope of main()
    beta = 2

    if beta == 2:
        # This runs if the conditional is true
        charlie = 3
    else:
        # This runs if the conditional is false
        charlie = 4

if __name__ == "__main__":
    main()
