#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t length;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }

    length = strlen(path);
    if (strncmp(path, prefix, sizeof(prefix) - 1) == 0
        && length >= sizeof(suffix) - 1
        && strcmp(path + length - (sizeof(suffix) - 1), suffix) == 0) {
        return real_readlink("/proc/self/exe", buffer, size);
    }

    return real_readlink(path, buffer, size);
}
