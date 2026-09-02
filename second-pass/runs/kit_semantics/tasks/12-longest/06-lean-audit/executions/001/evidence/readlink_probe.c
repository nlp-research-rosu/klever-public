#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    errno = 0;
    ssize_t result = real_readlink(path, buffer, size);
    int saved_errno = errno;
    dprintf(
        STDERR_FILENO,
        "READLINK_PROBE path=%s result=%zd errno=%d\n",
        path,
        result,
        saved_errno
    );
    errno = saved_errno;
    return result;
}
