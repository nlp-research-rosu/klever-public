/*
 * Audit-container workaround: Lean 4.22 asks readlink("/proc/<getpid>/exe").
 * In this nested PID environment /proc exposes a different PID namespace,
 * while /proc/self/exe remains correct. Rewrite only that exact Linux
 * executable-discovery request.
 */
#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_numeric_exe(const char *path) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t prefix_len = sizeof(prefix) - 1;
    size_t path_len;
    size_t i;

    if (path == NULL || strncmp(path, prefix, prefix_len) != 0) {
        return 0;
    }
    path_len = strlen(path);
    if (path_len <= prefix_len + sizeof(suffix) - 1 ||
        strcmp(path + path_len - (sizeof(suffix) - 1), suffix) != 0) {
        return 0;
    }
    for (i = prefix_len; i < path_len - (sizeof(suffix) - 1); ++i) {
        if (!isdigit((unsigned char)path[i])) {
            return 0;
        }
    }
    return 1;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_numeric_exe(path)) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}
