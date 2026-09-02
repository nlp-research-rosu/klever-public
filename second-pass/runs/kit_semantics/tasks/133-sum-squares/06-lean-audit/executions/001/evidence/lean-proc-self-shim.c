#define _GNU_SOURCE

#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc/self/exe but not /proc/<pid>/exe. Lean's
 * Linux runtime formats the latter with getpid(). Redirect only that exact
 * readlink request to the equivalent self alias.
 */
static const char *self_exe_alias(const char *path) {
    static __thread char expected[64];
    if (path == NULL) {
        return path;
    }
    int length = snprintf(expected, sizeof(expected), "/proc/%ld/exe",
                          (long)getpid());
    if (length > 0 && (size_t)length < sizeof(expected) &&
        strcmp(path, expected) == 0) {
        return "/proc/self/exe";
    }
    return path;
}

ssize_t readlink(const char *restrict path, char *restrict buffer,
                 size_t buffer_size) {
    return syscall(SYS_readlinkat, AT_FDCWD, self_exe_alias(path), buffer,
                   buffer_size);
}

ssize_t readlinkat(int directory_fd, const char *restrict path,
                   char *restrict buffer, size_t buffer_size) {
    return syscall(SYS_readlinkat, directory_fd, self_exe_alias(path), buffer,
                   buffer_size);
}
