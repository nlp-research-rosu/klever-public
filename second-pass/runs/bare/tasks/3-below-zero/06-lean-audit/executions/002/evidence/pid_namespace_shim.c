/*
 * Audit-runner compatibility shim.
 *
 * The runner's getpid() is in an inner PID namespace while its mounted /proc
 * exposes outer PIDs. Lean 4.22 constructs /proc/<getpid()>/exe, so recover
 * the outer numeric PID from the kernel-provided /proc/self symlink.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(target)) {
        errno = ESRCH;
        return (pid_t)-1;
    }
    target[length] = '\0';
    char *end = NULL;
    long value = strtol(target, &end, 10);
    if (end == target || *end != '\0' || value <= 0 || value > INT_MAX) {
        errno = ESRCH;
        return (pid_t)-1;
    }
    return (pid_t)value;
}
