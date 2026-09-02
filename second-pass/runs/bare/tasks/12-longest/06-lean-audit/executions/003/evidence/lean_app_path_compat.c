#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t size) {
    static readlink_fn real_readlink;
    if (!real_readlink) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    ssize_t result = real_readlink(path, buf, size);
    if (result < 0 && errno == ENOENT
            && strncmp(path, "/proc/", 6) == 0
            && strstr(path + 6, "/exe") != NULL) {
        result = real_readlink("/proc/self/exe", buf, size);
    }
    return result;
}
