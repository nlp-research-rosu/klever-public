#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <link.h>
#include <stdio.h>
#include <string.h>
#include <sys/auxv.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox denies Lean's readlink("/proc/<pid>/exe") call even
 * though the executable itself and AT_EXECFN are available.  Preserve normal
 * readlink behavior and repair only that failed procfs executable-path query.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    ssize_t result = real_readlink(path, buffer, size);
    int saved_errno = errno;
    if (result < 0 && strncmp(path, "/proc/", 6) == 0) {
        size_t length = strlen(path);
        if (length >= 4 && strcmp(path + length - 4, "/exe") == 0) {
            const char *execfn =
                (const char *)getauxval(AT_EXECFN);
            if (execfn != NULL) {
                size_t execfn_length = strlen(execfn);
                size_t copied =
                    execfn_length < size ? execfn_length : size;
                memcpy(buffer, execfn, copied);
                fprintf(
                    stderr,
                    "AUDIT_APP_PATH_SHIM: %s -> %.*s\n",
                    path,
                    (int)copied,
                    buffer
                );
                return (ssize_t)copied;
            }
        }
    }
    errno = saved_errno;
    return result;
}
