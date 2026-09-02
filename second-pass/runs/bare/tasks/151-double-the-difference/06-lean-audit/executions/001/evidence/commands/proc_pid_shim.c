#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit command sandbox exposes /proc from the outer PID namespace while
 * getpid() reports the inner namespace PID. Lean 4.22 resolves its executable
 * through /proc/<getpid()>/exe, so return the PID represented by /proc/self.
 */
pid_t getpid(void) {
    char buffer[64];
    ssize_t length = readlink("/proc/self", buffer, sizeof(buffer) - 1);
    if (length > 0 && length < (ssize_t)sizeof(buffer)) {
        buffer[length] = '\0';
        char *end = NULL;
        errno = 0;
        long value = strtol(buffer, &end, 10);
        if (errno == 0 && end != buffer && *end == '\0'
            && value > 0 && value <= INT_MAX) {
            return (pid_t)value;
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
