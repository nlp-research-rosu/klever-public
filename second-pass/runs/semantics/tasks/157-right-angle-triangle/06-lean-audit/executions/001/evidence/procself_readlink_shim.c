#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_function)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_function real_readlink = NULL;
    if (real_readlink == NULL) {
        real_readlink = (readlink_function)dlsym(RTLD_NEXT, "readlink");
    }

    char numeric_self[128];
    snprintf(numeric_self, sizeof(numeric_self), "/proc/%d/exe", getpid());
    if (strcmp(path, numeric_self) == 0) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
