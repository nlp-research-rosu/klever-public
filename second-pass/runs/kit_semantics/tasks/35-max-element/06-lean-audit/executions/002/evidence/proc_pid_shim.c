#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox exposes a host /proc mount while getpid() returns the
 * namespace-local PID. Lean 4.22 resolves its executable as /proc/PID/exe.
 * Return the host PID exposed by /proc/self so that lookup is well-defined.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(target)) {
        return (pid_t)1;
    }
    target[length] = '\0';
    errno = 0;
    char *end = NULL;
    long value = strtol(target, &end, 10);
    if (errno != 0 || end == target || *end != '\0' || value <= 0 || value > INT_MAX) {
        return (pid_t)1;
    }
    return (pid_t)value;
}
