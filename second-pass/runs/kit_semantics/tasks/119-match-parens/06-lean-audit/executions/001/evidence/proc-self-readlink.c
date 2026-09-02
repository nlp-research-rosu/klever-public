#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_numeric_proc_exe(const char *path) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    const size_t prefix_len = sizeof(prefix) - 1;
    const size_t suffix_len = sizeof(suffix) - 1;
    const size_t path_len = strlen(path);

    if (path_len <= prefix_len + suffix_len ||
        strncmp(path, prefix, prefix_len) != 0 ||
        strcmp(path + path_len - suffix_len, suffix) != 0) {
        return 0;
    }
    for (size_t i = prefix_len; i < path_len - suffix_len; ++i) {
        if (path[i] < '0' || path[i] > '9') {
            return 0;
        }
    }
    return 1;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }

    ssize_t result = real_readlink(path, buffer, size);
    if (result < 0 && errno == ENOENT && is_numeric_proc_exe(path)) {
        result = real_readlink("/proc/self/exe", buffer, size);
    }
    return result;
}
