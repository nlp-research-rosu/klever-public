#define _GNU_SOURCE

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Lean 4.22 resolves its executable through /proc/<getpid()>/exe.
 * In this audit sandbox, getpid() returns the namespace PID while the
 * read-only /proc mount exposes host PIDs.  /proc/self remains correct.
 * Return that visible PID so Lean's executable lookup sees the same process.
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
