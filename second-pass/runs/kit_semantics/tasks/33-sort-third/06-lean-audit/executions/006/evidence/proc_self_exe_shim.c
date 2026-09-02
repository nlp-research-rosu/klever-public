#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

static int is_numeric_proc_exe(const char *path) {
    int consumed = 0;
    if (path == NULL) return 0;
    if (sscanf(path, "/proc/%*u/exe%n", &consumed) != 0) return 0;
    return consumed > 0 && path[consumed] == '\0';
}

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    if (is_numeric_proc_exe(path)) path = "/proc/self/exe";
    return real_readlink(path, buffer, size);
}

ssize_t readlinkat(
    int dirfd, const char *restrict path, char *restrict buffer, size_t size
) {
    static ssize_t (*real_readlinkat)(int, const char *, char *, size_t) = NULL;
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
        if (real_readlinkat == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    if (is_numeric_proc_exe(path)) {
        dirfd = AT_FDCWD;
        path = "/proc/self/exe";
    }
    return real_readlinkat(dirfd, path, buffer, size);
}
