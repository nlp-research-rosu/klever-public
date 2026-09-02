#define _GNU_SOURCE

#include <dlfcn.h>
#include <sys/types.h>
#include <unistd.h>

#include <stdio.h>
#include <string.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    char namespace_self[64];

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    snprintf(
        namespace_self,
        sizeof(namespace_self),
        "/proc/%ld/exe",
        (long)getpid()
    );
    if (strcmp(path, namespace_self) == 0) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
