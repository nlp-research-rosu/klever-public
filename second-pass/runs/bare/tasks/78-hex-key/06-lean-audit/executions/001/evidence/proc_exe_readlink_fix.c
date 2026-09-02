#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t length;

    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    length = strlen(path);
    return length > sizeof(prefix) + sizeof(suffix) - 2
        && strcmp(path + length - (sizeof(suffix) - 1), suffix) == 0;
}

ssize_t readlink(const char *restrict path,
                 char *restrict buffer,
                 size_t buffer_size) {
    const char *resolved = is_proc_pid_exe(path) ? "/proc/self/exe" : path;
    return syscall(SYS_readlinkat, AT_FDCWD, resolved, buffer, buffer_size);
}

ssize_t readlinkat(int directory_fd,
                   const char *restrict path,
                   char *restrict buffer,
                   size_t buffer_size) {
    if (is_proc_pid_exe(path)) {
        directory_fd = AT_FDCWD;
        path = "/proc/self/exe";
    }
    return syscall(SYS_readlinkat, directory_fd, path, buffer, buffer_size);
}
