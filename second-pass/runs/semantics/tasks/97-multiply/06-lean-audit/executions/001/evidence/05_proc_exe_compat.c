#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
    static const char prefix[] = "/proc/";
    const char *cursor;
    if (strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    cursor = path + sizeof(prefix) - 1;
    if (*cursor < '0' || *cursor > '9') {
        return 0;
    }
    while (*cursor >= '0' && *cursor <= '9') {
        cursor++;
    }
    return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_pid_exe(path)) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
