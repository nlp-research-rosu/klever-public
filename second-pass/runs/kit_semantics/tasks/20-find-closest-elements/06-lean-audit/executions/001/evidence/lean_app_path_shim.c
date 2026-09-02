#define _GNU_SOURCE
#include <lean/lean.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox's PID namespace is not reflected in its read-only /proc
 * mount. Lean's lean_io_app_path therefore cannot read /proc/<pid>/exe.
 * Supply only that path from an explicit environment variable.
 */
lean_obj_res lean_io_app_path(void) {
    const char *path = getenv("LEAN_APP_PATH_OVERRIDE");
    if (path == NULL || path[0] == '\0') {
        return lean_io_result_mk_error(
            lean_mk_io_user_error(
                lean_mk_string("LEAN_APP_PATH_OVERRIDE is unset")));
    }
    return lean_io_result_mk_ok(lean_mk_string(path));
}

/*
 * Lean 4.22's Linux primitive calls readlink("/proc/<pid>/exe", ...).
 * The shared-library-internal call is not interposable here, but readlink is.
 */
ssize_t readlink(const char *pathname, char *buffer, size_t size) {
    const char *override = getenv("LEAN_APP_PATH_OVERRIDE");
    const size_t pathname_len = strlen(pathname);
    if (override != NULL
        && strncmp(pathname, "/proc/", 6) == 0
        && pathname_len >= 10
        && strcmp(pathname + pathname_len - 4, "/exe") == 0) {
        const size_t override_len = strlen(override);
        const size_t copied = override_len < size ? override_len : size;
        memcpy(buffer, override, copied);
        return (ssize_t)copied;
    }
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    return real_readlink(pathname, buffer, size);
}
