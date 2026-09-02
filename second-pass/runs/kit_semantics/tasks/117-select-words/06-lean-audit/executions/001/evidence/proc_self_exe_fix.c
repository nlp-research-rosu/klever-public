#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc/self/exe but not /proc/<namespace-pid>/exe.
 * Lean 4.22 asks for the latter.  Redirect only that exact procfs shape to
 * /proc/self/exe so the pinned unmodified Lean binaries can locate themselves.
 */
static int is_proc_pid_exe(const char *path) {
    const char *cursor;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) return 0;
    cursor = path + 6;
    if (*cursor < '0' || *cursor > '9') return 0;
    while (*cursor >= '0' && *cursor <= '9') cursor++;
    return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static ssize_t (*next_readlink)(const char *, char *, size_t) = NULL;
    if (next_readlink == NULL) {
        next_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_pid_exe(path)) path = "/proc/self/exe";
    return next_readlink(path, buffer, size);
}
