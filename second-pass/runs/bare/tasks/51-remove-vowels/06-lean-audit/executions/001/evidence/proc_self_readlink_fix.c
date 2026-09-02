#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buffer, size_t size) {
    char broken_self_path[64];
    int length = snprintf(
        broken_self_path,
        sizeof(broken_self_path),
        "/proc/%d/exe",
        getpid()
    );
    const char *effective_path = path;
    if (
        length > 0
        && (size_t)length < sizeof(broken_self_path)
        && strcmp(path, broken_self_path) == 0
    ) {
        effective_path = "/proc/self/exe";
    }
    return syscall(
        SYS_readlinkat,
        AT_FDCWD,
        effective_path,
        buffer,
        size
    );
}
