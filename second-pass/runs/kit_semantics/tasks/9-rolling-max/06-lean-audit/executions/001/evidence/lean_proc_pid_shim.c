#define _GNU_SOURCE

#include <limits.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void) {
    char target[PATH_MAX];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length > 0) {
        target[length] = '\0';
        char *end = NULL;
        long host_pid = strtol(target, &end, 10);
        if (end != target && *end == '\0' && host_pid > 0) {
            return (pid_t)host_pid;
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
