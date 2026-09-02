#define _GNU_SOURCE
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

/*
 * Compatibility for a PID namespace whose /proc mount exposes host PIDs.
 * Lean resolves /proc/<getpid()>/exe; use the host PID exposed by /proc/self.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(target)) {
        return (pid_t)-1;
    }
    target[length] = '\0';
    return (pid_t)strtol(target, NULL, 10);
}
