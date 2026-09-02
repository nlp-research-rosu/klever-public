#define _GNU_SOURCE

#include <ctype.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * The audit PID namespace exposes /proc/self/exe but not /proc/<getpid()>/exe.
 * Lean 4.22's IO.appPath uses the latter. Redirect exactly that path shape.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    const char *cursor;

    if (path != NULL && strncmp(path, prefix, sizeof(prefix) - 1) == 0) {
        cursor = path + sizeof(prefix) - 1;
        if (isdigit((unsigned char)*cursor)) {
            while (isdigit((unsigned char)*cursor)) {
                ++cursor;
            }
            if (strcmp(cursor, suffix) == 0) {
                path = "/proc/self/exe";
            }
        }
    }
    return syscall(SYS_readlink, path, buffer, size);
}
