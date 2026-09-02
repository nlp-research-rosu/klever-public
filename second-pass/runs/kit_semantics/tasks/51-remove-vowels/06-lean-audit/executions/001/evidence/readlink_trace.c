#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (!real_readlink) real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    ssize_t result = real_readlink(path, buffer, size);
    int saved_errno = errno;
    fprintf(stderr, "TRACE readlink path=%s size=%zu result=%zd errno=%d\n",
            path ? path : "<null>", size, result, saved_errno);
    errno = saved_errno;
    return result;
}

ssize_t readlinkat(int fd, const char *path, char *buffer, size_t size) {
    static readlinkat_fn real_readlinkat;
    if (!real_readlinkat) real_readlinkat = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
    ssize_t result = real_readlinkat(fd, path, buffer, size);
    int saved_errno = errno;
    fprintf(stderr, "TRACE readlinkat fd=%d path=%s size=%zu result=%zd errno=%d\n",
            fd, path ? path : "<null>", size, result, saved_errno);
    errno = saved_errno;
    return result;
}
