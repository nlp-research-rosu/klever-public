#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit runner exposes /proc/self/exe but not /proc/<getpid()>/exe.
 * Lean 4.22 queries the latter. Redirect only that exact procfs shape.
 */
static int is_pid_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t n;
    size_t i;
    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    n = strlen(path);
    if (n <= sizeof(prefix) - 1 + sizeof(suffix) - 1 ||
        strcmp(path + n - (sizeof(suffix) - 1), suffix) != 0) {
        return 0;
    }
    for (i = sizeof(prefix) - 1; i < n - (sizeof(suffix) - 1); ++i) {
        if (path[i] < '0' || path[i] > '9') {
            return 0;
        }
    }
    return 1;
}

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (is_pid_exe(path)) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buf, bufsiz);
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (is_pid_exe(path)) {
        dirfd = AT_FDCWD;
        path = "/proc/self/exe";
    }
    return real_readlinkat(dirfd, path, buf, bufsiz);
}
