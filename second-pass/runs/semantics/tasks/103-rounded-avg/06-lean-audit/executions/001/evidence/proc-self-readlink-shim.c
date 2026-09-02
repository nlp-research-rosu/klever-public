#define _GNU_SOURCE

#include <ctype.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * The audit sandbox places the process in a PID namespace but mounts a /proc
 * view in which /proc/self exists and /proc/<namespace-pid> does not. Lean
 * 4.22 asks readlink("/proc/<getpid()>/exe"). Rewrite only that exact shape.
 */
ssize_t readlink(const char *path, char *buffer, size_t buffer_size) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    const char *cursor = path;
    int rewrite = 0;

    if (strncmp(cursor, prefix, sizeof(prefix) - 1) == 0) {
        cursor += sizeof(prefix) - 1;
        if (isdigit((unsigned char)*cursor)) {
            while (isdigit((unsigned char)*cursor)) {
                cursor++;
            }
            rewrite = strcmp(cursor, suffix) == 0;
        }
    }

    return syscall(
        SYS_readlinkat,
        AT_FDCWD,
        rewrite ? "/proc/self/exe" : path,
        buffer,
        buffer_size
    );
}
