#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Audit-container compatibility shim.
 *
 * Lean 4.22 asks readlink("/proc/<getpid()>/exe", ...), but the audit
 * container's mounted /proc does not expose namespace-local numeric PIDs.
 * The kernel-provided /proc/self/exe link remains correct.  Redirect only
 * this one lookup; every other readlink call is passed through unchanged.
 */
ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    char expected[64];

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }

    snprintf(expected, sizeof(expected), "/proc/%ld/exe", (long)getpid());
    if (strcmp(path, expected) == 0) {
        return real_readlink("/proc/self/exe", buf, bufsiz);
    }
    return real_readlink(path, buf, bufsiz);
}
