#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    const char *cursor;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) return 0;
    cursor = path + 6;
    if (*cursor < '0' || *cursor > '9') return 0;
    while (*cursor >= '0' && *cursor <= '9') cursor++;
    return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*next_readlink)(const char *, char *, size_t);
    if (next_readlink == NULL)
        next_readlink = dlsym(RTLD_NEXT, "readlink");
    return next_readlink(
        is_proc_pid_exe(path) ? "/proc/self/exe" : path,
        buffer,
        size
    );
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    static ssize_t (*next_readlinkat)(int, const char *, char *, size_t);
    if (next_readlinkat == NULL)
        next_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    return next_readlinkat(
        directory,
        is_proc_pid_exe(path) ? "/proc/self/exe" : path,
        buffer,
        size
    );
}

char *realpath(const char *path, char *resolved) {
    static char *(*next_realpath)(const char *, char *);
    if (next_realpath == NULL)
        next_realpath = dlsym(RTLD_NEXT, "realpath");
    return next_realpath(
        is_proc_pid_exe(path) ? "/proc/self/exe" : path,
        resolved
    );
}
