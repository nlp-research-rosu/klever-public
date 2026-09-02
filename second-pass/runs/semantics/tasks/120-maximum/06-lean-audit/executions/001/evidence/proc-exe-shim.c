#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

static int is_proc_exe_lookup(const char *path) {
    const char *cursor;

    if (strcmp(path, "/proc/self/exe") == 0 ||
        strcmp(path, "/proc/thread-self/exe") == 0) {
        return 1;
    }
    if (strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    cursor = path + 6;
    if (*cursor < '0' || *cursor > '9') {
        return 0;
    }
    while (*cursor >= '0' && *cursor <= '9') {
        cursor++;
    }
    return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t buffer_size) {
    typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
    static readlink_fn real_readlink;
    const char *override;
    size_t length;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    override = getenv("PROC_SELF_EXE_OVERRIDE");
    if (override != NULL && is_proc_exe_lookup(path)) {
        length = strlen(override);
        if (length > buffer_size) {
            length = buffer_size;
        }
        memcpy(buffer, override, length);
        return (ssize_t)length;
    }
    return real_readlink(path, buffer, buffer_size);
}
