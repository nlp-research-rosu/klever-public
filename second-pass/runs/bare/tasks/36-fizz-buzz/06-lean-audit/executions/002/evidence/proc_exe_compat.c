#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc/self/exe but its PID namespace does not
 * expose /proc/<getpid()>/exe. Lean 4.22 uses the latter spelling. Redirect
 * only a decimal-PID executable lookup; all other readlink calls are
 * delegated unchanged.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    const char *cursor;

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }

    if (path != NULL && strncmp(path, "/proc/", 6) == 0) {
        cursor = path + 6;
        if (*cursor >= '0' && *cursor <= '9') {
            while (*cursor >= '0' && *cursor <= '9') {
                cursor++;
            }
            if (strcmp(cursor, "/exe") == 0) {
                return real_readlink("/proc/self/exe", buffer, size);
            }
        }
    }

    return real_readlink(path, buffer, size);
}
