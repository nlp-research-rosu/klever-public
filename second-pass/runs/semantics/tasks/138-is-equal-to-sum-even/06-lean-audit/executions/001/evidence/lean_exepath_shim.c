#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    const char *fixed = getenv("AUDIT_LEAN_EXE_PATH");
    size_t path_length = strlen(path);
    int proc_exe = (
        strncmp(path, "/proc/", 6) == 0
        && path_length > 10
        && strcmp(path + path_length - 4, "/exe") == 0
    );
    if (fixed != NULL && proc_exe) {
        size_t length = strlen(fixed);
        if (length > size) {
            length = size;
        }
        memcpy(buffer, fixed, length);
        dprintf(STDERR_FILENO, "AUDIT_SHIM readlink(%s) -> %.*s\n",
                path, (int)length, buffer);
        return (ssize_t)length;
    }

    readlink_fn real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (real_readlink == NULL) {
        errno = ENOSYS;
        return -1;
    }
    ssize_t result = real_readlink(path, buffer, size);
    dprintf(STDERR_FILENO, "AUDIT_SHIM readlink(%s) -> result=%zd errno=%d\n",
            path, result, errno);
    return result;
}
