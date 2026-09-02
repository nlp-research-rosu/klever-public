#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn next_readlink;
    if (next_readlink == NULL) {
        next_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (strncmp(path, "/proc/", 6) == 0) {
        size_t length = strlen(path);
        if (length >= 10 && strcmp(path + length - 4, "/exe") == 0) {
            return next_readlink("/proc/self/exe", buffer, size);
        }
    }
    return next_readlink(path, buffer, size);
}
