#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

static int is_pid_exe_path(const char *path) {
    const char *cursor;
    if (strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    cursor = path + 6;
    if (*cursor < '0' || *cursor > '9') {
        return 0;
    }
    while (*cursor >= '0' && *cursor <= '9') {
        cursor++;
    }
    return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (!real_readlink) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    ssize_t result = real_readlink(path, buf, bufsiz);
    int saved_errno = errno;
    if (result < 0 && (saved_errno == ENOENT || saved_errno == EACCES) &&
        is_pid_exe_path(path)) {
        result = real_readlink("/proc/self/exe", buf, bufsiz);
        saved_errno = errno;
        fprintf(stderr, "TRACE fallback /proc/self/exe");
    }
    fprintf(stderr, "TRACE readlink(%s) = %zd errno=%d", path, result, saved_errno);
    if (result >= 0) {
        fprintf(stderr, " target=%.*s", (int) result, buf);
    }
    fputc('\n', stderr);
    errno = saved_errno;
    return result;
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);
    if (!real_readlinkat) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    ssize_t result = real_readlinkat(dirfd, path, buf, bufsiz);
    int saved_errno = errno;
    fprintf(stderr, "TRACE readlinkat(%d,%s) = %zd errno=%d", dirfd, path, result, saved_errno);
    if (result >= 0) {
        fprintf(stderr, " target=%.*s", (int) result, buf);
    }
    fputc('\n', stderr);
    errno = saved_errno;
    return result;
}
