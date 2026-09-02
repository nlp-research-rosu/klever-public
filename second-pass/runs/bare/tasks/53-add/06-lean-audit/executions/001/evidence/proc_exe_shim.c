#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox does not expose child PIDs in /proc, while Lean 4.22's
 * IO.appPath resolves /proc/<pid>/exe.  Intercept only that lookup and return
 * the corresponding executable from the already-installed pinned toolchain.
 */
extern char *program_invocation_short_name;

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn original;
    const char *prefix = "/proc/";
    size_t path_length = strlen(path);

    if (original == NULL) {
        original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
        if (original == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }

    if (
        strncmp(path, prefix, strlen(prefix)) == 0
        && path_length >= 4
        && strcmp(path + path_length - 4, "/exe") == 0
        && program_invocation_short_name != NULL
    ) {
        char target[PATH_MAX];
        int written = snprintf(
            target,
            sizeof(target),
            "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/%s",
            program_invocation_short_name
        );
        if (
            written > 0
            && (size_t)written < sizeof(target)
            && access(target, X_OK) == 0
        ) {
            size_t copy_length = (size_t)written < size
                ? (size_t)written
                : size;
            memcpy(buffer, target, copy_length);
            return (ssize_t)copy_length;
        }
    }

    return original(path, buffer, size);
}
