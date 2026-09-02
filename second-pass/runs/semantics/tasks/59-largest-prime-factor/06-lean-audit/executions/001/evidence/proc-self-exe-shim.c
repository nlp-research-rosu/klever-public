#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    const char *cursor;

    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    cursor = path + sizeof(prefix) - 1;
    if (*cursor < '0' || *cursor > '9') {
        return 0;
    }
    while (*cursor >= '0' && *cursor <= '9') {
        cursor++;
    }
    return strcmp(cursor, suffix) == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_pid_exe(path)) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}
