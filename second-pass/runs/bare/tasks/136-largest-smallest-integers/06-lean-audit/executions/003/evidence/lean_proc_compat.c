#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * Compatibility shim for the audit container's split PID-/proc namespaces.
 * Lean 4.22 asks readlink("/proc/<getpid()>/exe"); this container exposes
 * that executable only through the kernel-provided /proc/self/exe alias.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    const char *prefix = "/proc/";
    const char *suffix = "/exe";
    const char *cursor;

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (strncmp(path, prefix, strlen(prefix)) == 0) {
        cursor = path + strlen(prefix);
        while (*cursor >= '0' && *cursor <= '9') {
            ++cursor;
        }
        if (strcmp(cursor, suffix) == 0) {
            return real_readlink("/proc/self/exe", buffer, size);
        }
    }
    return real_readlink(path, buffer, size);
}
