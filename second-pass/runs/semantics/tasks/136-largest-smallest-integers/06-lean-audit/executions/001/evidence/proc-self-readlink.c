/*
 * Audit-environment compatibility shim.
 *
 * This container exposes namespace PIDs via getpid() but its /proc mount does
 * not expose /proc/<namespace-pid>/exe. Lean 4.22 uses that exact path to find
 * its executable. For readlink calls matching only /proc/<digits>/exe, use the
 * semantically equivalent /proc/self/exe path. All other readlink calls pass
 * through unchanged.
 */

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
    const char *cursor;

    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    cursor = path + sizeof(prefix) - 1;
    if (!isdigit((unsigned char)*cursor)) {
        return 0;
    }
    while (isdigit((unsigned char)*cursor)) {
        ++cursor;
    }
    return strcmp(cursor, suffix) == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn original = NULL;

    if (original == NULL) {
        original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_pid_exe(path)) {
        return original("/proc/self/exe", buffer, size);
    }
    return original(path, buffer, size);
}
