#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_short_name;

static int is_proc_exe_path(const char *path) {
    size_t length;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    length = strlen(path);
    return length >= 4 && strcmp(path + length - 4, "/exe") == 0;
}

static ssize_t pinned_app_path(char *buffer, size_t buffer_size) {
    const char *toolchain_bin = getenv("AUDIT_TOOLCHAIN_BIN");
    const char *name = program_invocation_short_name;
    char path[PATH_MAX];
    int length;

    if (toolchain_bin == NULL || name == NULL || strchr(name, '/') != NULL) {
        errno = ENOENT;
        return -1;
    }
    length = snprintf(path, sizeof(path), "%s/%s", toolchain_bin, name);
    if (length < 0 || (size_t)length >= sizeof(path)) {
        errno = ENAMETOOLONG;
        return -1;
    }
    if (buffer_size > 0) {
        size_t copied = (size_t)length < buffer_size
            ? (size_t)length
            : buffer_size;
        memcpy(buffer, path, copied);
    }
    return (ssize_t)((size_t)length < buffer_size
        ? (size_t)length
        : buffer_size);
}

ssize_t readlink(const char *path, char *buffer, size_t buffer_size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (is_proc_exe_path(path)) {
        return pinned_app_path(buffer, buffer_size);
    }
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (real_readlink == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return real_readlink(path, buffer, buffer_size);
}

ssize_t readlinkat(
    int directory_fd,
    const char *path,
    char *buffer,
    size_t buffer_size
) {
    static ssize_t (*real_readlinkat)(
        int, const char *, char *, size_t
    ) = NULL;
    if (is_proc_exe_path(path)) {
        return pinned_app_path(buffer, buffer_size);
    }
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (real_readlinkat == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return real_readlinkat(directory_fd, path, buffer, buffer_size);
}
