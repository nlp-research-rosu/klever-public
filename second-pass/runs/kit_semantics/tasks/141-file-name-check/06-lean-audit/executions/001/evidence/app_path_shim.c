#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <sys/auxv.h>
#include <unistd.h>

static int is_self_exe(const char *path) {
    if (path == NULL) {
        return 0;
    }
    if (strcmp(path, "/proc/self/exe") == 0) {
        return 1;
    }
    char expected[64];
    int length = snprintf(
        expected, sizeof(expected), "/proc/%ld/exe", (long)getpid()
    );
    return length > 0
        && (size_t)length < sizeof(expected)
        && strcmp(path, expected) == 0;
}

static ssize_t copy_execfn(char *buffer, size_t size) {
    const char *execfn = (const char *)getauxval(AT_EXECFN);
    if (execfn == NULL || execfn[0] == '\0') {
        errno = ENOENT;
        return -1;
    }
    size_t length = strlen(execfn);
    size_t copied = length < size ? length : size;
    if (copied != 0) {
        memcpy(buffer, execfn, copied);
    }
    return (ssize_t)copied;
}

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    if (is_self_exe(path)) {
        return copy_execfn(buffer, size);
    }
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (real_readlink == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return real_readlink(path, buffer, size);
}

ssize_t readlinkat(
    int dirfd,
    const char *restrict path,
    char *restrict buffer,
    size_t size
) {
    if (is_self_exe(path)) {
        return copy_execfn(buffer, size);
    }
    static ssize_t (*real_readlinkat)(
        int, const char *, char *, size_t
    ) = NULL;
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (real_readlinkat == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return real_readlinkat(dirfd, path, buffer, size);
}
