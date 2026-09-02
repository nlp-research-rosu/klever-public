#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox mounts /proc from a parent PID namespace: /proc/self/exe
 * works, while /proc/<sandbox-pid>/exe does not exist. Lean 4.22 uses the
 * latter form. This preload shim changes only that readlink path.
 */
typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }

    const char *cursor = path;
    if (strncmp(cursor, "/proc/", 6) == 0) {
        cursor += 6;
        const char *digits = cursor;
        while (isdigit((unsigned char)*cursor)) {
            cursor++;
        }
        if (cursor > digits && strcmp(cursor, "/exe") == 0) {
            path = "/proc/self/exe";
        }
    }
    return real_readlink(path, buffer, size);
}
