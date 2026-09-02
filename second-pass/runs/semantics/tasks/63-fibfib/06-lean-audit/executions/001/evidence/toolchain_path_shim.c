#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit launcher exposes /proc from outside the process PID namespace:
 * /proc/self/exe resolves, but /proc/<getpid()>/exe does not. Lean 4.22 uses
 * the latter form. Redirect only that executable-path lookup.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    const char *suffix;

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (path != NULL && strncmp(path, "/proc/", 6) == 0) {
        suffix = strrchr(path, '/');
        if (suffix != NULL && strcmp(suffix, "/exe") == 0) {
            return real_readlink("/proc/self/exe", buffer, size);
        }
    }
    return real_readlink(path, buffer, size);
}
