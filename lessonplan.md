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
11. Memory Corruption Vulnerabilities
12. Other Vulnerabilities
13. Mitigations and Bypasses

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

There are three ways to work with python:

1. The Interpreter
2. A Script
3. Through the Argument

### The Interpreter

To launch an interactive interpreter, you can simply run the `python` command in
the terminal.

```bash
wheatley@ctf101-shell:~/ctf101$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Now, you may interact with the python interpreter by typing python statements
and pressing enter to evaluate the statement immediately.

```bash
wheatley@ctf101-shell:~/ctf101$ python
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

```
>>> exit()
wheatley@ctf101-shell:~/ctf101$ ipython
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

### A Script

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
wheatley@ctf101-shell:~/ctf101$ python sample.py
Name: Wheatley Robot
Your name is Wheatley Robot
wheatley@ctf101-shell:~/ctf101$
```

### Through the Argument

Sometimes if what we need to do is terse enough to do in a single line of
python, we may opt to pass the python code as an argument to the python program.
This lets us create nifty one liners to use in terminal trickery.

```bash
wheatley@ctf101-shell:~/ctf101$ python -c 'print "Clone\n"*10'
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

wheatley@ctf101-shell:~/ctf101$
```

- How to invoke python (cmd, interpreter, script)

- Language syntax
- Important module use

## 3. Input/Output

- Arguments
- Stdin/Stdout/Stderr
- Files
- Sockets

## 4. Types of Compromise

## 5. Illustration of Compromise in Target Python Applications

## 6. Data Representation and Endianness

## 7. C and x86-64 Assembly

## 8. Memory Layout

## 9. Stack Frames

## 10. Calling Conventions

## 11. Memory Corruption Vulnerabilities

## 12. Other Vulnerabilities

## 13. Mitigations and Bypasses


