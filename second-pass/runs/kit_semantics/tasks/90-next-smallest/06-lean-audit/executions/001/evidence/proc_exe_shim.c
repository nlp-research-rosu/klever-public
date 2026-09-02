#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_numeric_proc_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t length;
    size_t index;

    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    length = strlen(path);
    if (length <= (sizeof(prefix) - 1) + (sizeof(suffix) - 1) ||
        strcmp(path + length - (sizeof(suffix) - 1), suffix) != 0) {
        return 0;
    }
    for (index = sizeof(prefix) - 1;
         index < length - (sizeof(suffix) - 1);
         ++index) {
        if (path[index] < '0' || path[index] > '9') {
            return 0;
        }
    }
    return 1;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn original = NULL;
    const char *replacement;
    size_t length;

    if (is_numeric_proc_exe(path)) {
        replacement = getenv("AUDIT_LEAN_EXE_PATH");
        if (replacement == NULL || replacement[0] == '\0') {
            errno = ENOENT;
            return -1;
        }
        length = strlen(replacement);
        if (length > size) {
            length = size;
        }
        memcpy(buffer, replacement, length);
        return (ssize_t)length;
    }
    if (original == NULL) {
        original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
        if (original == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    return original(path, buffer, size);
}
