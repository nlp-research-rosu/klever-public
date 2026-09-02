/*
 * Compatibility shim for this audit sandbox's PID namespace.
 *
 * Lean 4.22 asks for /proc/<namespace-pid>/exe, while the read-only /proc
 * mounted by the audit runner exposes the process only through /proc/self.
 * Rewrite only that exact executable-link shape; all other reads are passed
 * through unchanged.
 */

#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
    const char *prefix = "/proc/";
    const char *suffix = "/exe";
    size_t prefix_len = strlen(prefix);
    if (path == NULL || strncmp(path, prefix, prefix_len) != 0) {
        return 0;
    }
    const char *cursor = path + prefix_len;
    if (!isdigit((unsigned char)*cursor)) {
        return 0;
    }
    while (isdigit((unsigned char)*cursor)) {
        cursor++;
    }
    return strcmp(cursor, suffix) == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    return real_readlink(
        is_proc_pid_exe(path) ? "/proc/self/exe" : path,
        buffer,
        size
    );
}

ssize_t readlinkat(
    int directory,
    const char *path,
    char *buffer,
    size_t size
) {
    static ssize_t (*real_readlinkat)(
        int,
        const char *,
        char *,
        size_t
    );
    if (real_readlinkat == NULL) {
        real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (is_proc_pid_exe(path)) {
        directory = AT_FDCWD;
        path = "/proc/self/exe";
    }
    return real_readlinkat(directory, path, buffer, size);
}
