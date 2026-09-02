#define _GNU_SOURCE
#include <fcntl.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buffer, size_t size) {
    const char *effective = path;
    size_t length = strlen(path);
    if (strncmp(path, "/proc/", 6) == 0 &&
        length >= 4 &&
        strcmp(path + length - 4, "/exe") == 0 &&
        strcmp(path, "/proc/self/exe") != 0) {
        effective = "/proc/self/exe";
    }
    return syscall(SYS_readlinkat, AT_FDCWD, effective, buffer, size);
}
