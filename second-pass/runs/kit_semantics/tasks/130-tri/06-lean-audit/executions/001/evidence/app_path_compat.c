#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdint.h>
#include <string.h>
#include <sys/auxv.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    size_t path_length = strlen(path);
    if (strcmp(path, "/proc/self/exe") == 0 ||
        (strncmp(path, "/proc/", 6) == 0 &&
         path_length >= 10 &&
         strcmp(path + path_length - 4, "/exe") == 0)) {
        const char *application = (const char *)getauxval(AT_EXECFN);
        if (application != NULL) {
            size_t length = strlen(application);
            if (length > size) {
                length = size;
            }
            memcpy(buffer, application, length);
            return (ssize_t)length;
        }
    }
    if (real_readlink == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return real_readlink(path, buffer, size);
}
