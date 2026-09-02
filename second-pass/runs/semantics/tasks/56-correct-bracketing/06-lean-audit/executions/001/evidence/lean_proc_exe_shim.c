#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc/self/exe but not /proc/<numeric-pid>/exe.
 * Lean 4.22's lean_io_app_path uses the latter. Redirect only that lookup.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    size_t length = strlen(path);
    if (
        length > 10
        && strncmp(path, "/proc/", 6) == 0
        && strcmp(path + length - 4, "/exe") == 0
        && strcmp(path, "/proc/self/exe") != 0
    ) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
