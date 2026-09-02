#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    char process_executable[64];
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    snprintf(
        process_executable,
        sizeof(process_executable),
        "/proc/%d/exe",
        getpid()
    );
    const char *resolved_path =
        strcmp(path, process_executable) == 0 ? "/proc/self/exe" : path;
    ssize_t result = real_readlink(resolved_path, buffer, size);
    int saved_errno = errno;
    dprintf(
        STDERR_FILENO,
        "AUDIT READLINK path=%s resolved=%s result=%zd errno=%d pid=%d\n",
        path,
        resolved_path,
        result,
        saved_errno,
        getpid()
    );
    errno = saved_errno;
    return result;
}
