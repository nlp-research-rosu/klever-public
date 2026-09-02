#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox returns a PID-namespace value from getpid(), while its
 * /proc mount is indexed by the outer PID. Lean 4.22 reads
 * /proc/<getpid()>/exe. Return the numeric target of /proc/self so Lean sees
 * the PID used by the mounted /proc. Fall back to the real getpid syscall.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length > 0 && length < (ssize_t)sizeof(target)) {
        target[length] = '\0';
        char *end = NULL;
        errno = 0;
        long value = strtol(target, &end, 10);
        if (errno == 0 && end != target && *end == '\0'
                && value > 0 && value <= INT_MAX) {
            return (pid_t)value;
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
