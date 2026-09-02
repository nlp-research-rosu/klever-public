#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The execution sandbox reports a namespace-local PID from getpid(), while
 * /proc is mounted with host PIDs. Lean 4.22 constructs /proc/<pid>/exe and
 * therefore cannot discover its own executable. Redirect only that Linux proc
 * lookup to the kernel-supported /proc/self/exe spelling.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (
        path != NULL
        && strncmp(path, "/proc/", 6) == 0
        && strlen(path) >= 4
        && strcmp(path + strlen(path) - 4, "/exe") == 0
    ) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}
