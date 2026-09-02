#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc/self/exe but not /proc/<numeric-pid>/exe.
 * Lean 4.22 constructs the numeric form. Rewrite only that one lookup.
 */
ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    const char *prefix = "/proc/";
    const char *suffix = "/exe";
    const char *cursor;

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (strncmp(path, prefix, strlen(prefix)) == 0) {
        cursor = path + strlen(prefix);
        if (*cursor >= '0' && *cursor <= '9') {
            while (*cursor >= '0' && *cursor <= '9') {
                cursor++;
            }
            if (strcmp(cursor, suffix) == 0) {
                path = "/proc/self/exe";
            }
        }
    }
    return real_readlink(path, buffer, size);
}
