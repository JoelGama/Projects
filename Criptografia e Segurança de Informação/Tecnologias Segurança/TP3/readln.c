#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

ssize_t readln(int fildes, void *buf, ssize_t nbyte) {
    ssize_t res = 0;
    int i = 0;

    while(i < nbyte && (res = read(fildes, &buf[i],1)) > 0) {
        if (((char *) buf)[i] == '\n') {
            return i;
        }
        i += res;
    }

    return i;
}