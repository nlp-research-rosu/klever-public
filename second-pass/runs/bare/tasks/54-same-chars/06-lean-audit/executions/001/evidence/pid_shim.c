#define _GNU_SOURCE

#include <limits.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Audit-container workaround only: getpid() returns a namespace PID while the
 * mounted /proc exposes host PIDs. Lean uses /proc/<getpid()>/exe to locate
 * its installation. /proc/self resolves to the current process's host PID.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length > 0 && length < (ssize_t)sizeof(target)) {
        target[length] = '\0';
        char *end = NULL;
        long observed = strtol(target, &end, 10);
        if (end != target && *end == '\0' && observed > 0
            && observed <= INT_MAX) {
            return (pid_t)observed;
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
