#define _GNU_SOURCE

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void) {
    char target[PATH_MAX];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(target)) {
        errno = ENOSYS;
        return (pid_t)-1;
    }
    target[length] = '\0';
    char *end = NULL;
    long visible_pid = strtol(target, &end, 10);
    if (end == target || *end != '\0' || visible_pid <= 0) {
        errno = ENOSYS;
        return (pid_t)-1;
    }
    return (pid_t)visible_pid;
}
