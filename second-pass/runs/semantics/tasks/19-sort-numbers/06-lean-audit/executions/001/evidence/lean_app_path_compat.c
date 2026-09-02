#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_name;

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_exe(const char *path) {
    const char *suffix;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    suffix = strrchr(path, '/');
    return suffix != NULL && strcmp(suffix, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    const char *application;
    size_t length;

    if (!is_proc_exe(path)) {
        if (real_readlink == NULL) {
            real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
        }
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
        return real_readlink(path, buffer, size);
    }

    application = program_invocation_name;
    if (application == NULL || application[0] != '/') {
        errno = ENOENT;
        return -1;
    }
    length = strlen(application);
    if (length > size) {
        length = size;
    }
    memcpy(buffer, application, length);
    return (ssize_t)length;
}
