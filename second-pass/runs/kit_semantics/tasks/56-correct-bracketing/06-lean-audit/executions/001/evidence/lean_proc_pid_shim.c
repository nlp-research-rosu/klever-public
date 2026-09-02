#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <unistd.h>

/*
 * Audit-sandbox compatibility only: Lean 4.22 resolves its executable via
 * /proc/<getpid()>/exe, while this launcher exposes host /proc but getpid()
 * returns a nested-namespace PID. /proc/self is a host-PID symlink here.
 */
pid_t getpid(void) {
    char target[PATH_MAX];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(target)) {
        _exit(126);
    }
    target[length] = '\0';
    char *end = NULL;
    errno = 0;
    long value = strtol(target, &end, 10);
    if (errno != 0 || end == target || *end != '\0' || value <= 0) {
        _exit(126);
    }
    return (pid_t)value;
}
