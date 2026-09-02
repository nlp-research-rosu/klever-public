#define _GNU_SOURCE

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Audit-sandbox compatibility shim.
 *
 * The sandbox exposes /proc from its parent PID namespace but getpid() from
 * its child PID namespace. Lean 4.22 constructs /proc/<getpid>/exe instead of
 * using /proc/self/exe, so IO.appPath fails. /proc/self is a symlink whose
 * target is the parent-namespace PID; return that PID to Lean.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(target)) {
        errno = ENOSYS;
        return (pid_t)-1;
    }
    target[length] = '\0';

    char *end = NULL;
    long value = strtol(target, &end, 10);
    if (end == target || *end != '\0' || value <= 0 || value > INT_MAX) {
        errno = ENOSYS;
        return (pid_t)-1;
    }
    return (pid_t)value;
}
