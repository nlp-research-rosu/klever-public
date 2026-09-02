#define _GNU_SOURCE
#include <fcntl.h>
#include <stddef.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Lean resolves its executable through /proc/<getpid>/exe.  In this audit
 * sandbox getpid() is PID-namespace local while /proc is host-mounted.
 * /proc/self/status exposes the host PID as "Pid", so return that value.
 */
pid_t getpid(void) {
    char buffer[4096];
    long descriptor = syscall(SYS_openat, AT_FDCWD, "/proc/self/status", O_RDONLY);
    if (descriptor < 0) {
        return (pid_t)syscall(SYS_getpid);
    }
    long length = syscall(SYS_read, descriptor, buffer, sizeof(buffer) - 1);
    syscall(SYS_close, descriptor);
    if (length <= 0) {
        return (pid_t)syscall(SYS_getpid);
    }
    buffer[length] = '\0';
    const char *cursor = buffer;
    while (*cursor != '\0') {
        if (cursor[0] == 'P' && cursor[1] == 'i' && cursor[2] == 'd' &&
            cursor[3] == ':') {
            cursor += 4;
            while (*cursor == ' ' || *cursor == '\t') {
                cursor++;
            }
            return (pid_t)strtol(cursor, NULL, 10);
        }
        while (*cursor != '\0' && *cursor != '\n') {
            cursor++;
        }
        if (*cursor == '\n') {
            cursor++;
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
