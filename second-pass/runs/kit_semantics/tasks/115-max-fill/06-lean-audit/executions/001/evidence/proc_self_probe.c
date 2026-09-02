#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    char buffer[PATH_MAX + 1];
    ssize_t size = readlink("/proc/self/exe", buffer, PATH_MAX);
    if (size < 0) {
        fprintf(stderr, "readlink failed: errno=%d (%s)\n", errno, strerror(errno));
        return 1;
    }
    buffer[size] = '\0';
    printf("pid=%ld executable=%s\n", (long)getpid(), buffer);
    return 0;
}
