#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdint.h>
#include <string.h>
#include <sys/auxv.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

static ssize_t copy_execfn(char *buffer, size_t size) {
    const char *path = (const char *)getauxval(AT_EXECFN);
    if (path == NULL) {
        errno = ENOENT;
        return -1;
    }
    size_t length = strlen(path);
    size_t copied = length < size ? length : size;
    memcpy(buffer, path, copied);
    return (ssize_t)copied;
}

static int is_proc_exe(const char *path) {
    size_t length = strlen(path);
    return strncmp(path, "/proc/", 6) == 0
        && length >= 10
        && strcmp(path + length - 4, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (is_proc_exe(path)) {
        return copy_execfn(buffer, size);
    }
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    return real_readlink(path, buffer, size);
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    static readlinkat_fn real_readlinkat;
    if (is_proc_exe(path)) {
        return copy_execfn(buffer, size);
    }
    if (real_readlinkat == NULL) {
        real_readlinkat = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
    }
    return real_readlinkat(directory, path, buffer, size);
}
