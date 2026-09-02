#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <sys/auxv.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Lean 4.22 queries /proc/<getpid()>/exe instead of /proc/self/exe.
 * The audit sandbox denies the former. For that one exact query, return
 * Linux's AT_EXECFN value. Delegate every other readlink call unchanged.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    char expected[64];
    const char *executable;
    size_t length;

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }

    snprintf(expected, sizeof(expected), "/proc/%ld/exe", (long)getpid());
    if (strcmp(path, expected) != 0) {
        return real_readlink(path, buffer, size);
    }

    executable = (const char *)getauxval(AT_EXECFN);
    if (executable == NULL || executable[0] == '\0') {
        return real_readlink(path, buffer, size);
    }
    length = strlen(executable);
    if (length > size) {
        length = size;
    }
    memcpy(buffer, executable, length);
    return (ssize_t)length;
}
