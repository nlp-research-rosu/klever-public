#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit launcher supplies a PID namespace but a host-PID /proc mount.
 * Lean 4.22 asks readlink("/proc/<getpid()>/exe", ...), which is therefore
 * absent. Redirect only that exact lookup to the namespace-safe self alias.
 */
ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    char lean_app_path[64];

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    snprintf(lean_app_path, sizeof(lean_app_path), "/proc/%ld/exe", (long)getpid());
    if (strcmp(path, lean_app_path) == 0) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
