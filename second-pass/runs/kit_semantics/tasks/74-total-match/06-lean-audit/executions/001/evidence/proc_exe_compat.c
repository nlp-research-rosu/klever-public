#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <stddef.h>
#include <unistd.h>

static int is_numeric_proc_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    const char *cursor = path;
    const char *expected = prefix;
    if (cursor == NULL) {
        return 0;
    }
    while (*expected != '\0') {
        if (*cursor++ != *expected++) {
            return 0;
        }
    }
    if (!isdigit((unsigned char)*cursor)) {
        return 0;
    }
    while (isdigit((unsigned char)*cursor)) {
        cursor++;
    }
    expected = suffix;
    while (*expected != '\0') {
        if (*cursor++ != *expected++) {
            return 0;
        }
    }
    return *cursor == '\0';
}

ssize_t readlink(const char *restrict path, char *restrict buffer,
                 size_t buffer_size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (is_numeric_proc_exe(path)) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, buffer_size);
}

ssize_t readlinkat(int directory_fd, const char *restrict path,
                   char *restrict buffer, size_t buffer_size) {
    static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (is_numeric_proc_exe(path)) {
        path = "/proc/self/exe";
    }
    return real_readlinkat(directory_fd, path, buffer, buffer_size);
}
