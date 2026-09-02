#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

static int is_numeric_proc_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    if (!path || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    const char *cursor = path + sizeof(prefix) - 1;
    if (!isdigit((unsigned char)*cursor)) {
        return 0;
    }
    while (isdigit((unsigned char)*cursor)) {
        cursor++;
    }
    return strcmp(cursor, suffix) == 0;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (!real_readlink) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (is_numeric_proc_exe(path)) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buf, size);
}
