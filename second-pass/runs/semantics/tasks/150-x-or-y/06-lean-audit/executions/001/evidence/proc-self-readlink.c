#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox virtualizes getpid() but exposes a host /proc mount, so
 * Lean's /proc/<getpid()>/exe lookup sees ENOENT. Redirect only that executable
 * lookup to the equivalent /proc/self/exe path.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    const size_t length = strlen(path);
    if (
        length > 10
        && strncmp(path, "/proc/", 6) == 0
        && strcmp(path + length - 4, "/exe") == 0
    ) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}
