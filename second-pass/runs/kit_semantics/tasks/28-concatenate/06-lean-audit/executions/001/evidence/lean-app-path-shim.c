#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <link.h>
#include <stdlib.h>
#include <string.h>
#include <sys/auxv.h>
#include <unistd.h>

static int is_proc_exe(const char *path) {
    const char *p;
    if (strcmp(path, "/proc/self/exe") == 0) {
        return 1;
    }
    if (strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    p = path + 6;
    if (*p < '0' || *p > '9') {
        return 0;
    }
    while (*p >= '0' && *p <= '9') {
        ++p;
    }
    return strcmp(p, "/exe") == 0;
}

static ssize_t copy_execfn(char *buffer, size_t size) {
    const char *execfn = (const char *)getauxval(AT_EXECFN);
    size_t length;
    if (execfn == NULL || *execfn == '\0') {
        errno = ENOENT;
        return -1;
    }
    length = strlen(execfn);
    if (length > size) {
        length = size;
    }
    memcpy(buffer, execfn, length);
    return (ssize_t)length;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (is_proc_exe(path)) {
        return copy_execfn(buffer, size);
    }
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    return real_readlink(path, buffer, size);
}

ssize_t readlinkat(
    int dirfd, const char *path, char *buffer, size_t size
) {
    static ssize_t (*real_readlinkat)(
        int, const char *, char *, size_t
    );
    if (path[0] == '/' && is_proc_exe(path)) {
        return copy_execfn(buffer, size);
    }
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    return real_readlinkat(dirfd, path, buffer, size);
}
