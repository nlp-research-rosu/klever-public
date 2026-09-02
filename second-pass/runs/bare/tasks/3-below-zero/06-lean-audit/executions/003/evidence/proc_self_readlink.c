#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    const char *cursor;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (strncmp(path, prefix, sizeof(prefix) - 1) == 0) {
        cursor = path + sizeof(prefix) - 1;
        while (*cursor >= '0' && *cursor <= '9') {
            cursor++;
        }
        if (strcmp(cursor, suffix) == 0) {
            path = "/proc/self/exe";
        }
    }
    return real_readlink(path, buffer, size);
}
