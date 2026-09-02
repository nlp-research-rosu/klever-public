#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn next_readlink = NULL;
    const char *prefix = "/proc/";
    const char *suffix = "/exe";
    const char *cursor;

    if (next_readlink == NULL) {
        next_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    cursor = path;
    if (cursor != NULL && strncmp(cursor, prefix, strlen(prefix)) == 0) {
        cursor += strlen(prefix);
        if (*cursor >= '0' && *cursor <= '9') {
            while (*cursor >= '0' && *cursor <= '9') {
                cursor++;
            }
            if (strcmp(cursor, suffix) == 0) {
                return next_readlink("/proc/self/exe", buffer, size);
            }
        }
    }
    return next_readlink(path, buffer, size);
}
