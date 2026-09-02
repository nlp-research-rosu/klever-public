#define _GNU_SOURCE

#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

extern char *program_invocation_name;

/*
 * The audit sandbox denies Lean's /proc/<own-pid>/exe readlink. Preserve the
 * real syscall everywhere, and use the current process invocation path only
 * for that one failed self lookup.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    ssize_t result = syscall(SYS_readlink, path, buffer, size);
    if (result >= 0) {
        return result;
    }

    char expected[64];
    int length = snprintf(
        expected, sizeof(expected), "/proc/%ld/exe", (long)getpid()
    );
    if (
        length <= 0
        || (size_t)length >= sizeof(expected)
        || strcmp(path, expected) != 0
        || program_invocation_name == NULL
    ) {
        return result;
    }

    const char *invocation = program_invocation_name;
    if (strcmp(invocation, "lean") == 0) {
        invocation =
            "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean";
    } else if (strcmp(invocation, "lake") == 0) {
        invocation =
            "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake";
    }

    size_t invocation_length = strlen(invocation);
    if (invocation_length > size) {
        invocation_length = size;
    }
    memcpy(buffer, invocation, invocation_length);
    errno = 0;
    return (ssize_t)invocation_length;
}
