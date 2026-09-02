#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    char expected[64];

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    snprintf(expected, sizeof(expected), "/proc/%ld/exe", (long)getpid());
    if (strcmp(path, expected) == 0) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}
