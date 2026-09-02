#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }

    ssize_t result = real_readlink(path, buffer, size);
    if (result >= 0 || path == NULL) {
        return result;
    }
    size_t length = strlen(path);
    if (
        strncmp(path, "/proc/", 6) == 0
        && length >= 10
        && strcmp(path + length - 4, "/exe") == 0
    ) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return result;
}
