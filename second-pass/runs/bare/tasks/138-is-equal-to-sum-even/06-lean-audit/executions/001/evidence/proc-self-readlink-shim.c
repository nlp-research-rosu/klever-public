#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc/self but not /proc/<getpid()> in the same
 * PID namespace. Lean 4.22 asks for /proc/<getpid()>/exe. Redirect exactly
 * that lookup to /proc/self/exe so the pinned compiler can start.
 */
ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (!real_readlink) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    size_t len = strlen(path);
    if (
        len > sizeof("/proc//exe") - 1
        && strncmp(path, "/proc/", sizeof("/proc/") - 1) == 0
        && strcmp(path + len - (sizeof("/exe") - 1), "/exe") == 0
    ) {
        return real_readlink("/proc/self/exe", buf, bufsiz);
    }
    return real_readlink(path, buf, bufsiz);
}
