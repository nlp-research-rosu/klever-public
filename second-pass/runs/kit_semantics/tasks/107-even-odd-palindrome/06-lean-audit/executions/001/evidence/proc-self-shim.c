#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t length;
    size_t index;
    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    length = strlen(path);
    if (length <= sizeof(prefix) + sizeof(suffix) - 2 ||
        strcmp(path + length - (sizeof(suffix) - 1), suffix) != 0) {
        return 0;
    }
    for (index = sizeof(prefix) - 1;
         index < length - (sizeof(suffix) - 1);
         ++index) {
        if (path[index] < '0' || path[index] > '9') {
            return 0;
        }
    }
    return 1;
}

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    return real_readlink(
        is_proc_pid_exe(path) ? "/proc/self/exe" : path,
        buffer,
        size
    );
}
