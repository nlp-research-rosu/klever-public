#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

static int is_proc_exe(const char *path) {
    size_t length;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    length = strlen(path);
    return length >= 10 && strcmp(path + length - 4, "/exe") == 0;
}

static ssize_t copy_override(char *buffer, size_t size) {
    const char *override = getenv("AUDIT_LEAN_APP_PATH");
    size_t length;
    if (override == NULL) {
        errno = ENOENT;
        return -1;
    }
    length = strlen(override);
    if (length > size) {
        length = size;
    }
    memcpy(buffer, override, length);
    return (ssize_t)length;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn next_readlink = NULL;
    if (is_proc_exe(path)) {
        return copy_override(buffer, size);
    }
    if (next_readlink == NULL) {
        next_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    return next_readlink(path, buffer, size);
}

ssize_t readlinkat(int dirfd, const char *path, char *buffer, size_t size) {
    static readlinkat_fn next_readlinkat = NULL;
    if (is_proc_exe(path)) {
        return copy_override(buffer, size);
    }
    if (next_readlinkat == NULL) {
        next_readlinkat = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
    }
    return next_readlinkat(dirfd, path, buffer, size);
}
