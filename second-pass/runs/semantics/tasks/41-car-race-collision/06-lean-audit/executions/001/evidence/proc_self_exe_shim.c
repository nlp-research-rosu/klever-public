#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit container exposes /proc/self/exe but does not expose
 * /proc/<getpid()>/exe for the PID namespace value returned to Lean.
 * Lean 4.22's IO.appPath uses the latter spelling. Redirect only that
 * Linux executable-link lookup to the semantically identical self link.
 */
ssize_t readlink(const char *path, char *buffer, size_t buffer_size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    const char *suffix;
    const char *cursor;
    int pid_path = 0;

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (path != NULL && strncmp(path, "/proc/", 6) == 0) {
        cursor = path + 6;
        suffix = strstr(cursor, "/exe");
        if (suffix != NULL && suffix[4] == '\0' && suffix > cursor) {
            pid_path = 1;
            for (const char *digit = cursor; digit < suffix; ++digit) {
                if (*digit < '0' || *digit > '9') {
                    pid_path = 0;
                    break;
                }
            }
        }
    }
    return real_readlink(
        pid_path ? "/proc/self/exe" : path,
        buffer,
        buffer_size
    );
}
