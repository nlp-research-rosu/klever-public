#define _GNU_SOURCE

#include <stddef.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Audit-sandbox compatibility shim: Lean's libuv executable-path probe is
 * unavailable under the process wrapper.  Return only the explicitly pinned
 * toolchain executable path; do not interpose any compiler or filesystem API.
 */
int uv_exepath(char *buffer, size_t *size) {
    const char *path = getenv("AUDIT_LEAN_EXE_PATH");
    size_t length;

    if (path == NULL || size == NULL) {
        return -22;
    }
    length = strlen(path);
    if (buffer == NULL || *size <= length) {
        *size = length + 1;
        return -105;
    }
    memcpy(buffer, path, length + 1);
    *size = length;
    return 0;
}

static ssize_t copy_executable_path(char *buffer, size_t size) {
    const char *path = getenv("AUDIT_LEAN_EXE_PATH");
    size_t length;

    if (path == NULL) {
        return -1;
    }
    length = strlen(path);
    if (length > size) {
        length = size;
    }
    memcpy(buffer, path, length);
    return (ssize_t)length;
}

static int is_process_executable_link(const char *path) {
    size_t length = strlen(path);

    return strncmp(path, "/proc/", 6) == 0
        && length >= 10
        && strcmp(path + length - 4, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*next_readlink)(const char *, char *, size_t) = NULL;

    if (is_process_executable_link(path)) {
        return copy_executable_path(buffer, size);
    }
    if (next_readlink == NULL) {
        next_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    return next_readlink(path, buffer, size);
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    static ssize_t (*next_readlinkat)(int, const char *, char *, size_t) = NULL;

    if (is_process_executable_link(path)) {
        return copy_executable_path(buffer, size);
    }
    if (next_readlinkat == NULL) {
        next_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    return next_readlinkat(directory, path, buffer, size);
}
