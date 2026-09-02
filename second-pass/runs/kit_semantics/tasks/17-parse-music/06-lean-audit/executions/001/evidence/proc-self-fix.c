#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    const char *cursor;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
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

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_pid_exe(path)) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}

ssize_t readlinkat(int dirfd, const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (is_proc_pid_exe(path)) {
        dirfd = AT_FDCWD;
        path = "/proc/self/exe";
    }
    return real_readlinkat(dirfd, path, buffer, size);
}
