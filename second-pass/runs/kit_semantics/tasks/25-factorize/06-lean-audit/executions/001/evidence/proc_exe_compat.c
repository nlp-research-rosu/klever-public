#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Lean 4.22 resolves its executable through /proc/<getpid()>/exe.  The
 * managed audit sandbox exposes /proc/self/exe but not numeric PID entries.
 * Redirect only that exact procfs shape; all other readlink calls are
 * unchanged.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    const char *cursor;

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (strncmp(path, "/proc/", 6) == 0) {
        cursor = path + 6;
        while (*cursor >= '0' && *cursor <= '9') {
            cursor++;
        }
        if (cursor > path + 6 && strcmp(cursor, "/exe") == 0) {
            path = "/proc/self/exe";
        }
    }
    return real_readlink(path, buffer, size);
}
