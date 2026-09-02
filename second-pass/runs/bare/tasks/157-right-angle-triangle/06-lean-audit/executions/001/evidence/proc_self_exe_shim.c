#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

/*
 * The audit sandbox's PID namespace is not the namespace mounted at /proc.
 * Lean 4.22 uses readlink("/proc/<getpid()>/exe") for IO.appPath. Redirect
 * exactly that numeric path shape to the namespace-independent self alias.
 */
ssize_t readlink(const char *path, char *buffer, size_t buffer_size) {
    static readlink_fn real_readlink = NULL;
    const char *effective_path = path;

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }

    if (path != NULL && strncmp(path, "/proc/", 6) == 0) {
        const char *cursor = path + 6;
        const char *digits = cursor;
        while (*cursor >= '0' && *cursor <= '9') {
            ++cursor;
        }
        if (cursor > digits && strcmp(cursor, "/exe") == 0) {
            effective_path = "/proc/self/exe";
        }
    }

    return real_readlink(effective_path, buffer, buffer_size);
}
