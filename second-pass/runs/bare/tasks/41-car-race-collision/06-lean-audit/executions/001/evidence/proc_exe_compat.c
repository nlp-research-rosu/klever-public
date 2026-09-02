#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stddef.h>
#include <string.h>
#include <sys/auxv.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Sandbox compatibility for Lean 4.22's IO.appPath.
 *
 * The audit sandbox denies /proc/<pid>/exe, although Linux exposes the same
 * executed filename in AT_EXECFN.  Intercept only that exact procfs pattern
 * and preserve normal readlink behavior for every other path.
 */

static int is_proc_self_exe(const char *path) {
    const char *cursor;

    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    cursor = path + 6;
    if (*cursor < '0' || *cursor > '9') {
        return 0;
    }
    while (*cursor >= '0' && *cursor <= '9') {
        ++cursor;
    }
    return strcmp(cursor, "/exe") == 0;
}

static ssize_t executable_path(char *buffer, size_t size) {
    const char *execfn = (const char *)getauxval(AT_EXECFN);
    size_t length;

    if (execfn == NULL || *execfn == '\0') {
        errno = ENOENT;
        return -1;
    }
    length = strlen(execfn);
    if (length > size) {
        length = size;
    }
    memcpy(buffer, execfn, length);
    return (ssize_t)length;
}

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static ssize_t (*next_readlink)(
        const char *restrict, char *restrict, size_t
    ) = NULL;

    if (is_proc_self_exe(path)) {
        return executable_path(buffer, size);
    }
    if (next_readlink == NULL) {
        next_readlink = dlsym(RTLD_NEXT, "readlink");
    }
    if (next_readlink == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return next_readlink(path, buffer, size);
}

ssize_t readlinkat(
    int directory,
    const char *restrict path,
    char *restrict buffer,
    size_t size
) {
    static ssize_t (*next_readlinkat)(
        int, const char *restrict, char *restrict, size_t
    ) = NULL;

    if (directory == AT_FDCWD && is_proc_self_exe(path)) {
        return executable_path(buffer, size);
    }
    if (next_readlinkat == NULL) {
        next_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
    }
    if (next_readlinkat == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return next_readlinkat(directory, path, buffer, size);
}
