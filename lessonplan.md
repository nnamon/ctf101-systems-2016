#ctf101 Systems 2016 Lesson Plan

## Assumptions

We assume that participants have the following pre-requisite knowledge:

1. Basic programming in any scripting language
2. Some elementary familiarity with C
3. The tools and ability to ssh into their provided shell accounts given out the
previous day

## Topics to Cover

0. Approach
1. Overview of Systems Exploitation
2. Offensive Python 101
3. Input/Output
4. Types of Compromise
5. Illustration of Compromise in Target Python Applications
6. Data Representation and Endianness
7. C and x86-64 Assembly
8. Memory Layout
9. Stack Frames
10. Calling Conventions
11. Debuggers
12. Memory Corruption Vulnerabilities
13. Other Vulnerabilities
14. Mitigations and Bypasses

## 0. Approach

In this session, we shift our focus from web technologies to systems
applications. These refer to applications that run 'natively' on your machines
or on remote machines. For example, programs like calc.exe or /bin/ls fall under
the category of systems applications. We will be learning how to delve deep into
the inner workings of these programs, discovering vulnerabilities, and
exploiting these vulnerabilities to achieve a compromise objective.

We will take an extremely incremental approach to the lesson where our approach
to the vulnerability discovery and exploit writing process is applied to easy
to understand vulnerable Python scripts before tackling compiled binaries that
require the extra step of reverse engineering of x86-64 assembly and an
understanding of memory layout.

It is hoped that by the end of the workshop, participants will have the required
knowledge of the tools and skills needed to further progress onto more advanced
topics in the reverse engineering and exploitation of systems applications.

Please do refer to this lesson plan for all code snippets and references as the
lesson progresses.

## 1. Overview of Systems Exploitation

Systems security is an extremely large domain. Basically, anything that runs on
a system, local or remote, is considered a systems application. Typically, the
primary target we look at in systems security are 'binaries'. These are compiled
applications that run natively on the processor of the machine. These binaries
could have been written in a variety of languages such as Golang or OCaml, but
most are probably written in C or C++. The important point to note here is that
obtaining an understanding of what the program does is not as simple as opening
the file in a text editor and hoping for the source code to appear. The result
is literally a 'binary' mess.

What is to be done then is to transform the raw native bytecode that make up the
binary into something understandable by a human. In this workshop, we will look
at turning the bytecode into x86-64 assembly in a process called disassembly.
The mapping between the raw bytecode and x86-64 instructions is sufficiently
close enough to understand what happens to the processor during program
execution. We will go further in depth into assembly language later on.

Vulnerabilities in these binaries come in two flavours: memory corruption and
logic vulnerabilties. Memory corruption vulnerabilties typically stem from a bug
in the code that provides a vector for an attacker to corrupt regions of memory
in such a way that the new values cause unintended consequences during program
execution. Logic vulnerabilities cause unintended consequences directly as a
result of faulty programming logic.

Interpreted programs such as ruby scripts or compiled Java bytecode also fall
under our domain. However, they primarily only contain logic vulnerabilities
(there might be extremely esoteric counterexamples, though).

We will craft our exploit code in the python language. Hopefully most of you are
already familiar with it but we will begin with a short crash course on the
language and required features of it.

## 2. Offensive Python 101

The following code snippets assume the shell environment you have been given
during the previous session.

### Working with Python

There are three ways to work with python:

1. The Interpreter
2. A Script
3. Through the Argument

#### The Interpreter

To launch an interactive interpreter, you can simply run the `python` command in
the terminal.

```bash
elliot@ctf101-shell:~/ctf101$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>
```

Now, you may interact with the python interpreter by typing python statements
and pressing enter to evaluate the statement immediately.

```bash
elliot@ctf101-shell:~/ctf101$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 1 + 41
42
>>> print "Here's looking at you, " + "kid."
Here's looking at you, kid.
>>> bin(1337)
'0b10100111001'
>>>
```

This is extremely useful when prototyping your exploits since you can get
feedback about what is happening in real time by exploring python objects.

```bash
>>> people = "Soylent Green is people!"
>>> dir(people)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__',
'__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__',
'__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__',
'__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
'__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__',
'__subclasshook__', '_formatter_field_name_split', '_formatter_parser',
'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs',
'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower',
'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip',
'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit',
'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title',
'translate', 'upper', 'zfill']
>>> people.upper()
'SOYLENT GREEN IS PEOPLE!'
>>>
```

However, we want to do something better. We now exit from the python interpreter
by typing `exit()` and launch the iPython interpreter. This upgraded interpreter
has quality of life improvements such colourised output, tab completion, and
object introspection. To launch it type `ipython`:

```bash
>>> exit()
elliot@ctf101-shell:~/ctf101$ ipython
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
Type "copyright", "credits" or "license" for more information.

IPython 2.4.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: import md5

In [2]: md5.
md5.blocksize    md5.digest_size  md5.md5          md5.new          md5.warnings

In [2]: hashed = md5.md5("password")

In [3]: hashed.
hashed.block_size   hashed.digest       hashed.digestsize   hashed.name
hashed.copy         hashed.digest_size  hashed.hexdigest    hashed.update

In [3]: hashed.hexdigest()
Out[3]: '5f4dcc3b5aa765d61d8327deb882cf99'

In [4]:
```

#### A Script

Typing so much all the time is not very useful for actual work though and we can
place our python programs in scripts. Launch your favourite text editor and
create the following [program](./lessonfiles/offensivepython/1-sample.py) as
`sample.py`:

```python
#!/usr/bin/python

def main():
    name = raw_input("Name: ")
    print "Your name is", name

if __name__ == "__main__":
    main()
```

Run the script by entering `python sample.py` in the terminal.

```bash
elliot@ctf101-shell:~/ctf101$ python sample.py
Name: Mr Robot
Your name is Mr Robot
elliot@ctf101-shell:~/ctf101$
```

#### Through the Argument

Sometimes if what we need to do is terse enough to do in a single line of
python, we may opt to pass the python code as an argument to the python program.
This lets us create nifty one liners for use in terminal trickery.

```bash
elliot@ctf101-shell:~/ctf101$ python -c 'print "Clone\n"*10'
Clone
Clone
Clone
Clone
Clone
Clone
Clone
Clone
Clone
Clone

elliot@ctf101-shell:~/ctf101$
```

Why would you use this option? For example, you might want to get something
quick and easy output for piping into another program.

```bash
elliot@ctf101-shell:~/ctf101$ python -c 'print "MrRobot"*42' | md5sum
827eae4fb606cf49ccaf8fc6b65cfdae  -
```

### Language syntax

We will go through a quick run through of the Python syntax you need to know for
our purposes.

#### Script Skeleton

Use the following template as a base for all python scripts:

```python
#!/usr/bin/python

def main():
    pass    # Code goes in here

if __name__ == "__main__":
    main()
```

The reason we do this is to keep our code neat and structured by ensuring all
functions and global variables are defined before we use them as python
interprets each line sequentially.

#### Whitespace

If you have not already noticed, python is extremely sensitive to whitespace.
This allows the language to do away with braces or start-end sigils by
implicitly determining the scope of a particular piece of code by the
indentation level.

```python
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
```

Make sure to not mix tabs and spaces for indentation as python will complain
about it.

#### Variables

You have already seen this but let us expand on this a little further. Python is
a dynamically typed language which means there is no requirement to declare the
type of a variable while writing your script. Objects do have types, however.
Think of the variable as a generic 'reference' to these typed objects.

```python
#!/usr/bin/python

# Creating a 'global' variable
var_global = 1337

def main():
    # Creating a variable that holds an integer
    var_one = 54321

    # Creating two variables that hold strings
    var_two = "I am a string"
    var_three = 'I too am a string, even though my quotes are single'

    # Creating a list object
    var_four = []

    # Creating a dict object
    var_five = {}

    # Creating a tuple object with two integers
    var_six = (41, 42)

    # Creating a file object from /etc/passwd
    var_seven = open("/etc/passwd")

    # Printing the contents of the file object by referencing a method
    print var_seven.read()



if __name__ == "__main__":
    main()
```

#### Conditionals

Conditionals allow for branching logic in a program and are an integral part of
every programming language. Here is how they look like in python:

```python
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
```

#### Loops

There are your traditional for and while loops in python:

```python
#!/usr/bin/python

import random

def main():
    # range() produces a list of numbers
    print range(10)
    # should produce [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # We use this in for loops to create our indexed for loops
    for i in range(10):
        print "This number is", i

    # If you have not already realised the for loop is actually a for-each loop
    travellers = ["Morty", "Rick", "Summer"]
    for i in travellers:
        if i is not "Summer":
            print i, ", you are are allowed to travel in time."
        else:
            print "Go away, Summer."

    # There are also while loops
    counter = 0
    while counter < 10:
        counter += random.randint(0, 5)  # Add a random integer to the counter
        print counter

    # Do while loops do not exist but can be approximated
    while True:
        counter = counter - 1
        if counter < 0:
            print "Stopped!"
            break

if __name__ == "__main__":
    main()
```

And there exists also a convenient feature of python called list comprehensions.
Please do not worry if the following is hard to follow:

```python
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
```

#### List and String Slicing

Lists are straightforward and creating sublists is extremely easy with slices.

```python
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
```

Strings also work with slices to create substrings.

```python
#!/usr/bin/python

def main():
    # The cake is a lie
    birthday_party = "The cake is a lie"

    cake = birthday_party[4:8]
    print cake  # Result is cake

    reverse = birthday_party[::-1]
    print reverse  # Result is eil a si ekac ehT

if __name__ == "__main__":
    main()
```

#### String Operations and Encoding

Some important string operations make for fast writing of exploits with how
convenient they are to use.

```python
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
```

Here are some encodings and transformations that might be useful:

```python
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
```

#### Functions

Finally, we come to functions which allow you to organise your program a lot
better.

```python
#!/usr/bin/python

def alone():
    print "I am alone."

def feed(food):
    print "I am fed", food

def add(a, b):
    return a + b

def main():
    # We can call a function with no parameters
    alone()

    # Or we can call it with a parameter
    feed("tacos")

    # Functions can be nested
    print add(add(1, 2), 3)

if __name__ == "__main__":
    main()
```

### Important Modules

Throughout the workshop, we will introduce important python modules as we
require. Modules are external 'libraries' that we import for use in our scripts.
We use the syntax `import <modulename>` to import a module.

## 3. Input/Output

Every interesting program requires some interaction with the user. Input/output
mechanisms give us this means of interaction and often, I/O sources are the very
first place to look at when trying to figure out how to cause a crash from user
supplied input.

### Arguments

The first way a program may take input is through its arguments. Let us use the
ping command as an example.

```bash
elliot@ctf101-shell:~$ ping -h
Usage: ping [-aAbBdDfhLnOqrRUvV] [-c count] [-i interval] [-I interface]
            [-m mark] [-M pmtudisc_option] [-l preload] [-p pattern] [-Q tos]
            [-s packetsize] [-S sndbuf] [-t ttl] [-T timestamp_option]
            [-w deadline] [-W timeout] [hop1 ...] destination
```

The help argument (-h) tells the ping command to print the available options for
arguments. In this case, the destination to ping is required as an argument.

```bash
elliot@ctf101-shell:~$ ping google.com
PING google.com (74.125.200.138) 56(84) bytes of data.
64 bytes from sa-in-f138.1e.net (74.125.200.138): icmp_seq=1 ttl=50 time=3.15 ms
64 bytes from sa-in-f138.1e.net (74.125.200.138): icmp_seq=2 ttl=50 time=2.96 ms
64 bytes from sa-in-f138.1e.net (74.125.200.138): icmp_seq=3 ttl=50 time=3.10 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 2.969/3.079/3.159/0.080 ms
elliot@ctf101-shell:~$
```

Sometimes you want to provide spaces within an argument. For example, you want
to create one file called "cool file" but when you try it by using the touch
program, two files called 'cool' and 'file' are created instead.

```bash
elliot@ctf101-shell:~/myfiles$ touch cool file
elliot@ctf101-shell:~/myfiles$ ls -la
total 8
drwxr-xr-x 2 elliot ctf101 4096 Aug 18 18:37 .
drwxr-xr-x 4 elliot ctf101 4096 Aug 18 18:37 ..
-rw-r--r-- 1 elliot ctf101    0 Aug 18 18:37 cool
-rw-r--r-- 1 elliot ctf101    0 Aug 18 18:37 file
elliot@ctf101-shell:~/myfiles$
```

We can remedy this by using quotes to treat whatever is in between them as a
single argument to the program.

```bash
elliot@ctf101-shell:~/myfiles$ touch 'cool file'
elliot@ctf101-shell:~/myfiles$ ls -la
total 8
drwxr-xr-x 2 elliot ctf101 4096 Aug 18 18:38 .
drwxr-xr-x 4 elliot ctf101 4096 Aug 18 18:37 ..
-rw-r--r-- 1 elliot ctf101    0 Aug 18 18:38 cool file
elliot@ctf101-shell:~/myfiles$
```

Now, let us consider the situation where you would like to programmatically
compute the argument instead of giving the program a static argument each time.
Perhaps, in this scenario you would like to rename the file to the md5 hash of
its contents. We can employ the use of backticks (`) in bash to achieve this.

```bash
elliot@ctf101-shell:~/myfiles$ ls -la 'cool file'
-rw-r--r-- 1 elliot ctf101 0 Aug 18 18:38 cool file
elliot@ctf101-shell:~/myfiles$ md5sum 'cool file' | cut -c -32
d41d8cd98f00b204e9800998ecf8427e
elliot@ctf101-shell:~/myfiles$ mv 'cool file' `md5sum 'cool file' | cut -c -32`
elliot@ctf101-shell:~/myfiles$ ls -la
total 8
drwxr-xr-x 2 elliot ctf101 4096 Aug 18 18:50 .
drwxr-xr-x 4 elliot ctf101 4096 Aug 18 18:37 ..
-rw-r--r-- 1 elliot ctf101    0 Aug 18 18:38 d41d8cd98f00b204e9800998ecf8427e
elliot@ctf101-shell:~/myfiles$
```

What if we want to execute a program through a python script? We can make use of
either the `os` or `subprocess` modules to perform this. Let's take a look at
the os module first:

```python
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
```

The `os.system()` function is basically a wrapper to run shell commands. There
is a big distinction to running a program within a shell and without as we will
see when we use the subprocess module instead. Running the program yields:

```bash
elliot@ctf101-shell:~/ctf101$ python argumentsos.py
f0ee0388ebfa8223e795491cb38a3081  /etc/issue.net
Hello, Friend
```

Checking that the file indeed exists within the current directory now:

```bash
elliot@ctf101-shell:~/ctf101$ ls -la badfile
total 20
-rw-r--r-- 1 elliot ctf101   14 Aug 19 06:38 badfile
elliot@ctf101-shell:~/ctf101$
```

Now, let us use the `subprocess` module.

```python
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
```

The special symbols that meant various things within the shell such as pipes,
backticks, redirections now are just passed directly to the program instead of
interpreted by the shell and will do nothing. Executing the python script:

```bash
elliot@ctf101-shell:~/ctf101$ python argumentsubprocess.py
f0ee0388ebfa8223e795491cb38a3081  /etc/issue.net
```
### Standard Streams

Another method of interacting with the user is through the standard streams:
`stdin`, `stdout`, and `stderr`. The stdin and stdout stream should be familiar
to you. Reading from `stdin` gets the input the user provides and writing to
`stdout` prints information back to the user. `stderr` provides a means for
programs to output debugging or error information without polluting the `stdout`
stream.

Remember the python interpreter we interacted with?

```bash
elliot@ctf101-shell:~/ctf101$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> "this is me sending data to the python program through stdin"
'this is me sending data to the python program through stdin'
>>>
```

We 'send' data through `stdin` to the program by typing in our shell and in turn
the program 'sends' data through `stdout` to us by printing it in our shell.

What about `stderr`? Error messages such as the following are written to
`stderr`:

```bash
elliot@ctf101-shell:~/ctf101$ ls -la /root
ls: cannot open directory '/root': Permission denied
```

How do you tell? First, we have to introduce the concept of pipes and stream
redirection. Often you would like for programs to interact with each other. You
have seen examples of this in some of the previous code snippets. Imagine
running a program and getting some output:

```bash
elliot@ctf101-shell:~/ctf101$ python -c 'print "A"*24'
AAAAAAAAAAAAAAAAAAAAAAAA
elliot@ctf101-shell:~/ctf101$
```

Now, we could copy the output by hand manually and paste it into another program
as a way to transfer this information. However, there is a better way. We can
join the `stdout` of the `python` program to the `stdin` of another program, say
`base64`. This is called 'piping' the output of our first program into the input
of a second program. The special symbol we use to do this is called the 'pipe'
(|).

```bash
elliot@ctf101-shell:~/ctf101$ python -c 'print "A"*24' | base64
QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBCg==
elliot@ctf101-shell:~/ctf101$
```

We can even chain more pipes to connect the output of `base64` to `md5sum`.

```bash
elliot@ctf101-shell:~/ctf101$ python -c 'print "A"*24' | base64 | md5sum
2aafa255bcb4d626dba2804faf55a16a  -
elliot@ctf101-shell:~/ctf101$
```

What if we want to redirect the output of a stream to another stream? We can do
this by using stream redirection. Going back to the `stderr` example, we can
make the output disappear by redirecting what comes out on `stderr` to the
special `/dev/null` device that ignores what is fed into it.

```bash
elliot@ctf101-shell:~/ctf101$ ls -la /root
ls: cannot open directory '/root': Permission denied
elliot@ctf101-shell:~/ctf101$ ls -la /root 2>/dev/null
elliot@ctf101-shell:~/ctf101$ ls -la /root 1>/dev/null
ls: cannot open directory '/root': Permission denied
```

Take note that the streams are given file descriptor numbers. 0 is `stdin`, 1 is
`stdout`, and 2 is `stderr`. So when we do `2>/dev/null` it makes the `stderr`
output go into the `/dev/null` device and disappear. Let us look at an example
with `grep`.

```bash
elliot@ctf101-shell:~/ctf101$ echo "hello world" | grep -c hello
1
elliot@ctf101-shell:~/ctf101$ echo "hello world" | grep -c goodbye
0
elliot@ctf101-shell:~/ctf101$
```

`grep` is a program that searches the input for the the string given in the
argument and if it matches, it outputs the number of matched occurences (due to
us applying the `-c` argument). Let us try this out on the `stderr` example.

```bash
elliot@ctf101-shell:~/ctf101$ ls -la /root
ls: cannot open directory '/root': Permission denied
elliot@ctf101-shell:~/ctf101$ ls -la /root | grep -c denied
ls: cannot open directory '/root': Permission denied
0
elliot@ctf101-shell:~/ctf101$
```

Notice that the error message is still printed out and the word denied is not
matched. If we redirect `stderr` to `stdout`, and grep for the word, it changes.

```bash
elliot@ctf101-shell:~/ctf101$ ls -la /root 2>&1 | grep -c denied
1
elliot@ctf101-shell:~/ctf101$
```

Note that `&1` refers to the file descriptor 1 which is `stdout`.

Remember our explorations with calling programs with python in the previous
section? What if we want to interact with our programs from that? The answer is
obviously manipulating these streams.

```python
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
```

Running the application:

```bash
elliot@ctf101-shell:~/ctf101$ python streams.py
aGVsbG8=

elliot@ctf101-shell:~/ctf101$
```

### Files

Some programs take filenames as arguments. The simplest of them is the `cat`
command which reads the file and prints the file contents to `stdout`.

```bash
elliot@ctf101-shell:~/ctf101$ cat /etc/issue.net
Ubuntu 16.04.1 LTS
elliot@ctf101-shell:~/ctf101$
```

With bash, you can also redirect the output of program to a file with the `>`
symbol.

```bash
elliot@ctf101-shell:~/ctf101$ echo "Contents of this file" > thisfile
elliot@ctf101-shell:~/ctf101$ cat thisfile
Contents of this file
elliot@ctf101-shell:~/ctf101$
```

You can also read files into the `stdin` of a program with the opposite symbol
`<`.

```bash
elliot@ctf101-shell:~/ctf101$ base64 < thisfile
Q29udGVudHMgb2YgdGhpcyBmaWxlCg==
elliot@ctf101-shell:~/ctf101$
```

In python, you can create, write to, and read from files as well.

```python
#!/usr/bin/python

def main():
    # Let's create a file
    towrite = open("my_file", "w")  # 'w' stands for open for write

    # Now, we can write a string into it
    towrite.write("some string")

    # Close the file
    towrite.close()

    # We can do the converse option by reading the file
    toread = open("my_file")  # implicitly open for read

    # Read the contents
    contents = toread.read()
    print contents

    # Close the file
    toread.close()

if __name__ == "__main__":
    main()
```

Running the script:

```bash
elliot@ctf101-shell:~/ctf101$ python files.py
some string
elliot@ctf101-shell:~/ctf101$
```

### Sockets

The majority of the exercises we will be going through involve interacting with
a service hosted on a different system. That is, we will be looking at obtaining
access to a remote system. First, we need to learn how to even begin connecting
to such a remote service. Netcat is an extremely useful command line tool that
lets you create arbitrary TCP or UDP sockets.

Obviously we know that web pages are served over the network but can we manually
obtain the home page of http://codesinverse.com? We can with netcat!

```bash
elliot@ctf101-shell:~/ctf101$ nc codesinverse.com 80
GET / HTTP/1.0

HTTP/1.1 200 OK
Date: Fri, 19 Aug 2016 11:20:30 GMT
Server: Apache/2.2.14 (Ubuntu)
Last-Modified: Sun, 27 Oct 2013 11:52:27 GMT
ETag: "3d01208-ed-4e9b79e1054c0"
Accept-Ranges: bytes
Content-Length: 237
Vary: Accept-Encoding
Connection: close
Content-Type: text/html

<head>
  <title>Codes^-1</title>
</head>
<body>
  <br />
  <br />
  <br />
  <div align="center">
    <h1>Q29kZXNpbnZlcnNlIGlzIHVuZGVyIGNvbnN0cnVjdGlvbiE=</h1>
    <h2>Smoke me a kipper, I'll be back for breakfast.</h2>
  </div>
</body>
elliot@ctf101-shell:~/ctf101$
```

Often, when you play in a CTF, the challenge description might contain something
like `nc pwn.spro.ink 1337`. Why not try it out?

```bash
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1337
What is your name? Elliot Alderson
Welcome Elliot Alderson, here's your flag: ctf101{1st_Fl4g_0f_th3_d4y!}
elliot@ctf101-shell:~/ctf101$
```

We can script this in python as well.

```python
#!/usr/bin/python

import socket

def main():
    # Create a socket
    sock = socket.socket()

    # Connect the socket to the remote service
    sock.connect(("pwn.spro.ink", 1337))

    # Receive the first prompt
    prompt = sock.recv(1024)  # Receive an arbitrary max 1024 bytes
    print prompt

    # Send our name
    sock.send("Elliot Alderson\n")  # Remember the newline at the end

    # Receive the flag
    flagline = sock.recv(1024)

    print flagline

if __name__ == "__main__":
    main()
```

Running the script:

```bash
elliot@ctf101-shell:~/ctf101$ python sockets.py
What is your name?
Welcome Elliot Alderson, here's your flag: ctf101{1st_Fl4g_0f_th3_d4y!}

elliot@ctf101-shell:~/ctf101$
```

That covers most of what you need to know about input/output for today. Let us
move on to the actual security stuff from this point on.

## 4. Types of Compromise

Keep in mind that we are still dealing with extremely high level and abstract
concepts at this point of the workshop. Some of the high level goals of an
attacker include the following (in ascending order of severity and control):

1. Denial of Service
2. Information Leakage
3. Arbitrary File Read
4. Arbitrary File Write
5. Remote Code Execution
6. Privilege Escalation

### Denial of Service

Denial of Service vulnerabilities are broad and can be categorised as
destructive or non-destructive. The common theme between them is that they
obstruct and prevent legitimate users from accessing a service or resource.
While Denial of Service attacks can be caused by congestion of network
resources, we focus more on the vulnerabilties that exist inherently in the
application logic.

The most common denial of service conditions come from the program behind the
service crashing due to an exception such a segmentation fault. Another possible
reason why a service might not be responsive is because a particular resource
(such as memory) might be exhausted. This is evident when people launch fork
bombs in a shell.

### Information Leakage

An information leak (infoleak, for short) is a vulnerability that, when
exploited, reveals privileged information about the system or application to an
attacker. The effects of this information being in the control of an attacker
can be varying. Information an attack might be interested in include:

- Password Hashes
- Source Code
- Binaries
- Pointers and Addresses
- libc Shared Object

While infoleaks are not typically dangerous by themselves, they are used in
conjunction with another vulnerability to obtain more control over a system. We
distinguish this class with 'Arbitrary File Read' by restricting ourselves to
application specific features such as pointers that may exist in memory.

### Arbitrary File Read

Arbitrary file read vulnerabilities allow the attacker to retrieve any file that
the owner of the service has access to. The severity of an arbitrary file read
vulnerability varies based on the type of information granted to the attacker.
If SSH keys are left lying around, this vulnerability may as well be a remote
code execution one.

### Arbitrary File Write

Arbitrary file write vulnerabilties allow an attacker to create/overwrite files
on the file system with controlled content. Now, this is dangerous on multiple
levels. If the application is privileged and is capable of overwriting system
files such as /etc/shadow, /etc/passwd or even a user file such as
~/.ssh/authorized\_keys, an attacker may grant themselves access over SSH. If
the application is not privileged, but has write access to their own
directories, an attacker may insert content to perform arbitrary code execution.

An example of arbitrary code execution often appears when exploiting PHP web
applications where arbitrary PHP code is written to the file system and
triggered by the attacker when they surf to the location of the newly created
file.

### Remote Code Execution

Certain vulnerabilities grant arbitrary code execution which allows an attacker
to coerce the system into performing any operation she wishes. This may manifest
as a result of injection of evaluated data such as shell commands or scripts, or
on a more fundamental level such as taking control of the instruction pointer to
execute your own machine code. Arbitrary code execution is very closely tied to
privilege escalation where hijacking the control flow of a binary with
privileged access results in granting these privileges to the attacker.

### Privilege Escalation

Privilege escalation vulnerabilities can exist in multiple forms and are not
necessarily arbitrary code execution bugs. They often are though. These
vulnerabilties, when exploited result in the attacker obtaining higher level
rights such as administrator or root.

At a more advanced level, there exists vulnerabilities within the kernel of the
operating system. These vulnerabilities usually allow an attacker with local
access to the system to escalate their rights from a restricted user to root.

## 5. Illustration of Compromise in Target Python Applications

To make it easier to visualise and internalise these compromise goals, let us go
through a couple of examples in a high level script such as python where we try
to compromise a couple of remote services (where applicable).

### Denial of Service

To demonstrate this scalably, everyone will run an instance of the server on
their own shells. This means you should start up another terminal and log into
your shell again so you can play both the attacker and the attacked.

Please create the following python script:

```python
#!/usr/bin/python

import socket

def main():
    HOST, PORT = "localhost", 0

    # Create the server, binding to localhost on a free port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)

    # Print the connection information
    print "Please connect to %s %d" % (HOST, server.getsockname()[1])

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    while True:
        # Accept a connection
        conn, addr = server.accept()

        # Interact with the client
        conn.sendall("Please enter the number you wish to square: ")

        # Get the integer
        data = conn.recv(1024)
        number = int(data)

        # Square it
        square = number * number

        # Print the number back to the client as a string
        conn.sendall(str(square) + "\n")

        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
```

Run it in your newly created terminal, note the connection information and
return to your first terminal.

```bash
elliot@ctf101-shell:~/ctf101$ python denialofservice.py
Please connect to localhost 43065

```

Try interacting with the server normally.

```bash
elliot@ctf101-shell:~/ctf101$ nc localhost 43065
Please enter the number you wish to square: 23
529
elliot@ctf101-shell:~/ctf101$
```

Do this a couple of times to convince yourself that the server will work for
multiple people. Now, let us deny others the service by attempting to crash the
script. What happens when we pass the server a letter instead of a number?

```bash
elliot@ctf101-shell:~/ctf101$ nc localhost 43065
Please enter the number you wish to square: A
elliot@ctf101-shell:~/ctf101$ nc -v localhost 43065
nc: connect to localhost port 43065 (tcp) failed: Connection refused
elliot@ctf101-shell:~/ctf101$
```

Looks like the server is no longer accepting connections. If we check the
terminal where we ran the server we find that the script has terminated due to
an exception:

```bash
elliot@ctf101-shell:~/ctf101$ python denialofservice.py
Please connect to localhost 43065
Traceback (most recent call last):
  File "denialofservice.py", line 39, in <module>
    main()
  File "denialofservice.py", line 27, in main
    number = int(data)
ValueError: invalid literal for int() with base 10: 'A\n'
elliot@ctf101-shell:~/ctf101$
```

This is a straightforward exercise demonstrating how a crash caused by bad input
by a user to the server has prevented other legitimate users from accessing the
service.

### Information Leakage

Information leaks are very interesting vulnerabilities that allow you to leak
what goes on under the hood of the program. Take a look at the following script:

```python
#!/usr/bin/python

import sys

FLAG = open("/home/infoleak/flag")
PUBLIC_DATA = "RainRainGoAwayComeAgainAnotherDay"

def write(data):
    sys.stdout.write(data)
    sys.stdout.flush()

def main():
    haystack = FLAG + PUBLIC_DATA
    write("Welcome to the Infoleak!\n")
    write("Please enter an index: ")

    index = len(FLAG) + int(sys.stdin.readline())
    write("Giving you the data from index %d...\n" % index)
    write("Here's the data: %s\n" % haystack[index:])


if __name__ == "__main__":
    main()
```

Can you spot the vulnerability? The service is running at `nc pwn.spro.ink
1338`. Let's try interacting with it.

```bash
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1338
Welcome to the Infoleak!
Please enter an index: 0
Giving you the data from index 43...
Here's the data: RainRainGoAwayComeAgainAnotherDay
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1338
Welcome to the Infoleak!
Please enter an index: 10
Giving you the data from index 53...
Here's the data: AwayComeAgainAnotherDay
elliot@ctf101-shell:~/ctf101$
```

Now, certain things in the output should raise some red flags here. Notice how
when entering a zero index, we are given data from index 16. Now, looking back
at the source code, we can observe that the data comes from the 'haystack'
variable. This variable is a concatenation of the 'FLAG' and 'PUBLIC\_DATA' and
our supplied index is added to the length of 'FLAG' which means any 'legitimate'
value that we type will result in the calculated index landing within the 'safe'
public data.

You may not have recognised it, but our infoleak vulnerability occurs here:

```python
    index = len(FLAG) + int(sys.stdin.readline())
```

When supplying an index of zero, we can obtain the length of the flag. We'll use
this information later. Let's try to make the program behave in a non-intended
manner right now. Notice that the program is using int() to convert a string
into an integer. Most programming languages support inputs such as "1", "999",
and with some parameters, "4e3bc" but remember, negative integers are integers
too and are properly handled by these parsers. Let's see if it works:

```bash
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1338
Welcome to the Infoleak!
Please enter an index: -2
Giving you the data from index 41...
Here's the data: }
RainRainGoAwayComeAgainAnotherDay
elliot@ctf101-shell:~/ctf101$
```

And it does! Supplying a negative integer will allow us to read data from the
non-public segment of the 'haystack'. It is just a matter of applying the
information of the flag length we obtained just now to get the entire flag.

```bash
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1338
Welcome to the Infoleak!
Please enter an index: -43
Giving you the data from index 0...
Here's the data: ctf101{w3ll_1_gu355_th3y_4r3_fl0ating_n0w}
RainRainGoAwayComeAgainAnotherDay
elliot@ctf101-shell:~/ctf101$
```

### Arbitrary File Read


### Arbitrary File Write


### Remote Code Execution


### Privilege Escalation



## 6. Data Representation and Endianness

- Numbering Systems: Decimal, Binary, Hexadecimal
- Data Representation: integers, word size, ascii, asciiz strings
- Endianness

## 7. C and x86-64 Assembly

- Compiling C
- Disassembling the binary
- Reading x86-64 assembly

## 8. Memory Layout

- Stack and Heap
- Variables - stack variables, dynamically allocated variables and static
  variables

## 9. Stack Frames

- Saved RIP
- Saved EBP

## 10. Calling Conventions

- stcall
- cdecl
- fastcall

## 11 Debuggers

- GDB
- Inputs
- Breakpoints
- Examining and modifying context
- Crash Analysis

## 12. Memory Corruption Vulnerabilities


## 13. Other Vulnerabilities

- Format string bugs
- Insecure paths
- Integer overflows
- Predictive randomisation

## 14. Mitigations and Bypasses

- Stack Canaries
- ASLR
- NX

## 15. Conclusion and Additional Challenges

This section brings the workshop to an end. We hope it was adequate in giving
you an introduction to the topics we covered and have sparked an interest in
vulnerability analysis and exploit writing. Stay tuned for workshops that cover
more advanced topics.

If time permits, please do try the following challenges out to test your
understanding of what we covered today and maybe explore a bit more on your own.

### Challenge 1

### Challenge 2

