#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <sys/auxv.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The managed audit PID namespace does not expose /proc/<getpid()>/exe even
 * though /proc/self/exe works for a separate readlink process. Lean 4.22 uses
 * the numeric spelling in IO.appPath. Answer only that one self-executable
 * lookup from AT_EXECFN; delegate every other readlink unchanged.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    char expected[64];
    int expected_length;
    const char *executable;
    size_t length;

    expected_length = snprintf(
        expected, sizeof(expected), "/proc/%ld/exe", (long)getpid()
    );
    if (
        expected_length > 0
        && (size_t)expected_length < sizeof(expected)
        && strcmp(path, expected) == 0
    ) {
        executable = (const char *)getauxval(AT_EXECFN);
        if (executable == NULL) {
            errno = ENOENT;
            return -1;
        }
        length = strlen(executable);
        if (length > size) {
            length = size;
        }
        memcpy(buffer, executable, length);
        return (ssize_t)length;
    }

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    return real_readlink(path, buffer, size);
}
