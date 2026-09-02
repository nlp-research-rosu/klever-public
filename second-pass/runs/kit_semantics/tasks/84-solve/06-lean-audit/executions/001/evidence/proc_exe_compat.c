#define _GNU_SOURCE
#include <ctype.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t prefix_len = sizeof(prefix) - 1;
    size_t suffix_len = sizeof(suffix) - 1;
    size_t length;
    size_t index;

    if (path == NULL || strncmp(path, prefix, prefix_len) != 0) {
        return 0;
    }
    length = strlen(path);
    if (length <= prefix_len + suffix_len ||
        strcmp(path + length - suffix_len, suffix) != 0) {
        return 0;
    }
    for (index = prefix_len; index < length - suffix_len; ++index) {
        if (!isdigit((unsigned char)path[index])) {
            return 0;
        }
    }
    return 1;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    const char *effective = is_proc_pid_exe(path) ? "/proc/self/exe" : path;
    return readlinkat(AT_FDCWD, effective, buffer, size);
}
