#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_function)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t buffer_size) {
    static readlink_function real_readlink;
    const char *selected_path = path;
    size_t length;

    if (real_readlink == NULL) {
        real_readlink = (readlink_function)dlsym(RTLD_NEXT, "readlink");
    }
    length = strlen(path);
    if (length > 10
        && strncmp(path, "/proc/", 6) == 0
        && strcmp(path + length - 4, "/exe") == 0) {
        selected_path = "/proc/self/exe";
    }
    return real_readlink(selected_path, buffer, buffer_size);
}
