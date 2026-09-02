#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    size_t length;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    length = strlen(path);
    return length >= 10 && strcmp(path + length - 4, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    ssize_t result = syscall(SYS_readlink, path, buffer, size);
    if (result < 0 && errno == ENOENT && is_proc_pid_exe(path)) {
        return syscall(SYS_readlink, "/proc/self/exe", buffer, size);
    }
    return result;
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    ssize_t result = syscall(SYS_readlinkat, directory, path, buffer, size);
    if (result < 0 && errno == ENOENT && is_proc_pid_exe(path)) {
        return syscall(
            SYS_readlinkat, AT_FDCWD, "/proc/self/exe", buffer, size
        );
    }
    return result;
}
