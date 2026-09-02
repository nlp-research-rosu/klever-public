#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Lean 4.22 resolves its executable through /proc/<getpid()>/exe.  The audit
 * sandbox exposes /proc/self/exe but not the PID-named alias.  Redirect only
 * that one executable lookup; every other readlink call is unchanged.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }

    const size_t length = strlen(path);
    if (length > 10 && strncmp(path, "/proc/", 6) == 0 &&
        strcmp(path + length - 4, "/exe") == 0) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
