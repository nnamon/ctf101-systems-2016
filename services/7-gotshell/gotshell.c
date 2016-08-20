#include <stdio.h>

// Compiled with gcc -m32 -fno-stack-protector -o gotshell gotshell.c

void giveshell() {
    system("/bin/sh");
}

void vuln() {
    char buffer[80];
    puts("Feed me"); // Print this
    fflush(NULL); // Flush stdout
    read(0, buffer, 200); // Read into the buffer
}

int main() {
    vuln();
}
