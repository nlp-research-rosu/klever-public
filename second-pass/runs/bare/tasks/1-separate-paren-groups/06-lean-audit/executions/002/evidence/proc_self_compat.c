#define _GNU_SOURCE

#include <dlfcn.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

static int is_numeric_proc_exe(const char *path) {
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
    static readlink_fn original;

    if (original == NULL) {
        original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (is_numeric_proc_exe(path)) {
        path = "/proc/self/exe";
    }
    return original(path, buffer, size);
}

ssize_t readlinkat(
    int directory,
    const char *path,
    char *buffer,
    size_t size
) {
    static readlinkat_fn original;

    if (original == NULL) {
        original = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
    }
    if (directory == AT_FDCWD && is_numeric_proc_exe(path)) {
        path = "/proc/self/exe";
    }
    return original(directory, path, buffer, size);
}
