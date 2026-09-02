#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
    ssize_t result = real_readlink(path, buf, size);
    if (result < 0 && path && strncmp(path, "/proc/", 6) == 0 &&
        strlen(path) > 10 &&
        strcmp(path + strlen(path) - 4, "/exe") == 0) {
        return real_readlink("/proc/self/exe", buf, size);
    }
    return result;
}
