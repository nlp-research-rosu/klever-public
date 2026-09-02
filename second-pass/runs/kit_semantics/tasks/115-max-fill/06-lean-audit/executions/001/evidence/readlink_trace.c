#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn actual;
    if (!actual) {
        actual = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    ssize_t result = actual(path, buffer, size);
    int saved_errno = errno;
    fprintf(stderr, "TRACE readlink(%s, size=%zu) -> %zd errno=%d",
            path ? path : "(null)", size, result, saved_errno);
    if (result >= 0) {
        fprintf(stderr, " target=%.*s", (int)result, buffer);
    }
    fputc('\n', stderr);
    errno = saved_errno;
    return result;
}
