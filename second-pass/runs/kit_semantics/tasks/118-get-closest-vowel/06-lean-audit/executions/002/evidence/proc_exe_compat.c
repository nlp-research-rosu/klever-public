#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
    const char *p;

    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
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

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static readlink_fn real_readlink;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    return real_readlink(is_proc_pid_exe(path) ? "/proc/self/exe" : path,
                         buf, bufsiz);
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t bufsiz) {
    static readlinkat_fn real_readlinkat;

    if (real_readlinkat == NULL) {
        real_readlinkat = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
    }
    if (is_proc_pid_exe(path)) {
        return real_readlinkat(AT_FDCWD, "/proc/self/exe", buf, bufsiz);
    }
    return real_readlinkat(dirfd, path, buf, bufsiz);
}
