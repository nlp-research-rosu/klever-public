#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

/*
 * The audit container's PID namespace can expose a process-local PID that has
 * no matching /proc/<pid>/exe entry. Lean 4.22 queries that numeric entry.
 * Translate that numeric self-PID form to the kernel's unambiguous
 * /proc/self/exe. Every other readlink path remains unchanged.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
    static readlink_fn real_readlink;
    if (!real_readlink) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (strncmp(path, "/proc/", 6) == 0) {
        const char *cursor = path + 6;
        if (*cursor >= '0' && *cursor <= '9') {
            while (*cursor >= '0' && *cursor <= '9') {
                cursor++;
            }
            if (strcmp(cursor, "/exe") == 0) {
                return real_readlink("/proc/self/exe", buf, size);
            }
        }
    }
    return real_readlink(path, buf, size);
}
