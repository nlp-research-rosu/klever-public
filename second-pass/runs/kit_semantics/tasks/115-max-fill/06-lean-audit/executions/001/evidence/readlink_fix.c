#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn actual;
    if (!actual) {
        actual = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (path && strncmp(path, "/proc/", 6) == 0) {
        const char *suffix = strrchr(path, '/');
        if (suffix && strcmp(suffix, "/exe") == 0) {
            return actual("/proc/self/exe", buffer, size);
        }
    }
    return actual(path, buffer, size);
}
