#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    const char *suffix;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    suffix = path == NULL ? NULL : strrchr(path, '/');
    if (path != NULL
        && strncmp(path, "/proc/", 6) == 0
        && suffix != NULL
        && strcmp(suffix, "/exe") == 0
        && strcmp(path, "/proc/self/exe") != 0) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}
