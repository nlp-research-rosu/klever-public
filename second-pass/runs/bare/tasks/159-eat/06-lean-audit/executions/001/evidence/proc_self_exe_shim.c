#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    const char *suffix = "/exe";
    size_t length;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }

    length = strlen(path);
    if (
        length > strlen("/proc//exe")
        && strncmp(path, "/proc/", strlen("/proc/")) == 0
        && strcmp(path + length - strlen(suffix), suffix) == 0
    ) {
        return real_readlink("/proc/self/exe", buffer, size);
    }

    return real_readlink(path, buffer, size);
}
