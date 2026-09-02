#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }

    const char *prefix = "/proc/";
    const char *suffix = "/exe";
    size_t length = strlen(path);
    size_t prefix_length = strlen(prefix);
    size_t suffix_length = strlen(suffix);
    if (length > prefix_length + suffix_length
        && strncmp(path, prefix, prefix_length) == 0
        && strcmp(path + length - suffix_length, suffix) == 0) {
        const char *cursor = path + prefix_length;
        const char *end = path + length - suffix_length;
        int numeric = cursor < end;
        while (cursor < end) {
            numeric = numeric && *cursor >= '0' && *cursor <= '9';
            cursor++;
        }
        if (numeric) {
            path = "/proc/self/exe";
        }
    }
    return real_readlink(path, buffer, size);
}
