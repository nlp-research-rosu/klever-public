#define _GNU_SOURCE

#include <ctype.h>
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t index = sizeof(prefix) - 1;

    if (strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    if (!isdigit((unsigned char)path[index])) {
        return 0;
    }
    while (isdigit((unsigned char)path[index])) {
        index++;
    }
    return strcmp(path + index, suffix) == 0;
}

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_pid_exe(path)) {
        return real_readlink("/proc/self/exe", buffer, size);
    }
    return real_readlink(path, buffer, size);
}
