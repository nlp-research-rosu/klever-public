#define _GNU_SOURCE

#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox denies readlink("/proc/<current-pid>/exe") while allowing
 * the equivalent "/proc/self/exe". Lean 4.22's IO.appPath uses the former.
 * Redirect only that exact self-PID request and leave every other readlink
 * unchanged.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    char self_pid_path[64];
    int length = snprintf(
        self_pid_path,
        sizeof(self_pid_path),
        "/proc/%ld/exe",
        (long)getpid()
    );
    const char *effective_path = path;
    if (
        length > 0
        && (size_t)length < sizeof(self_pid_path)
        && strcmp(path, self_pid_path) == 0
    ) {
        effective_path = "/proc/self/exe";
    }
    return syscall(SYS_readlink, effective_path, buffer, size);
}
