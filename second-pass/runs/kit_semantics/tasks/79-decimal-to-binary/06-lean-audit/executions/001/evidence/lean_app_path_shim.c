#define _GNU_SOURCE
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

static const char pinned_lean_path[] =
    "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean";

static int is_current_executable_link(const char *path) {
    char expected[64];
    if (path == NULL) {
        return 0;
    }
    snprintf(expected, sizeof(expected), "/proc/%ld/exe", (long)getpid());
    return strcmp(path, "/proc/self/exe") == 0 || strcmp(path, expected) == 0;
}

ssize_t readlink(const char *restrict path, char *restrict buffer,
                 size_t buffer_size) {
    if (is_current_executable_link(path)) {
        size_t length = strlen(pinned_lean_path);
        size_t copied = length < buffer_size ? length : buffer_size;
        memcpy(buffer, pinned_lean_path, copied);
        return (ssize_t)copied;
    }
    return syscall(SYS_readlink, path, buffer, buffer_size);
}

ssize_t readlinkat(int directory_fd, const char *restrict path,
                   char *restrict buffer, size_t buffer_size) {
    if (is_current_executable_link(path)) {
        size_t length = strlen(pinned_lean_path);
        size_t copied = length < buffer_size ? length : buffer_size;
        memcpy(buffer, pinned_lean_path, copied);
        return (ssize_t)copied;
    }
    return syscall(SYS_readlinkat, directory_fd, path, buffer, buffer_size);
}
