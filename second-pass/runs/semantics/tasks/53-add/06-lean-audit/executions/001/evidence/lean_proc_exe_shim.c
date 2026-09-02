#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    size_t length;
    size_t index;

    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    length = strlen(path);
    if (length <= sizeof(prefix) - 1 + sizeof(suffix) - 1 ||
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

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    if (is_proc_pid_exe(path)) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
