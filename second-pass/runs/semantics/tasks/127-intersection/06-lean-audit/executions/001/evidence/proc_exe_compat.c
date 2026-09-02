#define _GNU_SOURCE

#include <ctype.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    const char *cursor;

    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    cursor = path + sizeof(prefix) - 1;
    if (!isdigit((unsigned char)*cursor)) {
        return 0;
    }
    while (isdigit((unsigned char)*cursor)) {
        cursor++;
    }
    return strcmp(cursor, suffix) == 0;
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

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);

    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (is_proc_pid_exe(path)) {
        directory = AT_FDCWD;
        path = "/proc/self/exe";
    }
    return real_readlinkat(directory, path, buffer, size);
}
