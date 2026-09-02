#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Audit-sandbox compatibility shim: the sandbox unshares PID state without
 * mounting a matching /proc. Lean's runtime resolves /proc/<pid>/exe, which
 * therefore fails, while the kernel-provided /proc/self/exe link is valid.
 * Redirect only that executable-link lookup and leave every other readlink
 * unchanged.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    const size_t length = strlen(path);
    if (length > 10 && strncmp(path, "/proc/", 6) == 0 &&
        strcmp(path + length - 4, "/exe") == 0) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
