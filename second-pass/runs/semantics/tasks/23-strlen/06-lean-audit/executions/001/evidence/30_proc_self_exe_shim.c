#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <sys/auxv.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

static ssize_t executable_path(char *buffer, size_t size) {
    const char *path = (const char *)getauxval(AT_EXECFN);
    if (path == NULL || path[0] == '\0') {
        errno = ENOENT;
        return -1;
    }
    size_t length = strlen(path);
    size_t copied = length < size ? length : size;
    if (copied > 0) {
        memcpy(buffer, path, copied);
    }
    return (ssize_t)copied;
}

static int is_proc_executable_link(const char *path) {
    size_t length = strlen(path);
    return length >= 10
        && strncmp(path, "/proc/", 6) == 0
        && strcmp(path + length - 4, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    if (is_proc_executable_link(path)) {
        return executable_path(buffer, size);
    }
    static readlink_fn original;
    if (original == NULL) {
        original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    return original(path, buffer, size);
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    if (is_proc_executable_link(path)) {
        return executable_path(buffer, size);
    }
    static readlinkat_fn original;
    if (original == NULL) {
        original = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
    }
    return original(directory, path, buffer, size);
}
