#define _GNU_SOURCE

#include <ctype.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * The audit sandbox's getpid() is namespaced while /proc is host-mounted.
 * Lean 4.22 asks for /proc/<getpid()>/exe rather than /proc/self/exe.
 * Redirect only that exact path shape; all other readlink calls are unchanged.
 */
ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    const char *cursor;

    if (strncmp(path, prefix, sizeof(prefix) - 1) == 0) {
        cursor = path + sizeof(prefix) - 1;
        if (isdigit((unsigned char)*cursor)) {
            while (isdigit((unsigned char)*cursor)) {
                cursor++;
            }
            if (strcmp(cursor, suffix) == 0) {
                return syscall(SYS_readlink, "/proc/self/exe", buffer, size);
            }
        }
    }
    return syscall(SYS_readlink, path, buffer, size);
}
