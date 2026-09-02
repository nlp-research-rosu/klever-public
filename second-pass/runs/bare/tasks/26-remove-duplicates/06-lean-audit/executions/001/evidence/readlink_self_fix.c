/*
 * Sandbox-only compatibility shim for Lean 4.22 IO.appPath.
 *
 * This environment permits /proc/self/exe but denies
 * /proc/<numeric-current-pid>/exe. Rewrite only the latter exact path.
 */
#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    char current_process_exe[64];

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    snprintf(
        current_process_exe,
        sizeof(current_process_exe),
        "/proc/%ld/exe",
        (long)getpid()
    );
    if (strcmp(path, current_process_exe) == 0) {
        path = "/proc/self/exe";
    }
    return real_readlink(path, buffer, size);
}
