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
    if (check(user_pass, "ThisIsALongPassword")) {
        printf("Win!\n");
        setuid(0);
        system("/bin/sh");
    }
    else {
        printf("Fail!\n");
    }
}
