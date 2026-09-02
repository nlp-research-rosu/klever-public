#define _GNU_SOURCE

#include <limits.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox exposes a host-PID /proc mount while getpid() returns the
 * nested namespace PID. Lean 4.22 constructs /proc/<getpid()>/exe, so return
 * the numeric target of /proc/self for audited Lean/Lake subprocesses.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    long value = 0;

    if (length <= 0) {
        return (pid_t)1;
    }
    target[length] = '\0';
    for (ssize_t index = 0; index < length; ++index) {
        if (target[index] < '0' || target[index] > '9') {
            return (pid_t)1;
        }
        value = value * 10 + (target[index] - '0');
        if (value > INT_MAX) {
            return (pid_t)1;
        }
    }
    return (pid_t)value;
}
