#include<stdio.h>
#include<string.h>

#define MAX_FILE_NAME_CHARS 255

int main(int argc, char *argv[]) {
    FILE *fp;
    char file_name[MAX_FILE_NAME_CHARS];
    int ch;
    int i;

    if(argc<1){
        return 0;
    }

    strncpy(file_name, argv[i], MAX_FILE_NAME_CHARS);

    fp=fopen(argv[1], "r");
    if(fp == NULL) {
        printf("%s: No such file or directory\n", file_name);
        return 0;
    }

    while((ch=fgetc(fp)) != EOF){
        putchar(ch);
    }
    fclose(fp);
    return 0;
}
