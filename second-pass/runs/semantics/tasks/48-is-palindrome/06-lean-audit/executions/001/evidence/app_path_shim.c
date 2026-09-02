#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

extern char *program_invocation_short_name;

static int is_proc_exe_path(const char *path) {
    int pid = 0;
    char tail = '\0';
    return path != NULL
        && sscanf(path, "/proc/%d/exe%c", &pid, &tail) == 1
        && pid > 0;
}

static ssize_t supply_app_path(char *buffer, size_t size) {
    const char *directory = getenv("AUDIT_LEAN_BIN_DIR");
    const char *application = program_invocation_short_name;
    if (
        directory == NULL
        || directory[0] == '\0'
        || application == NULL
        || (
            strcmp(application, "lean") != 0
            && strcmp(application, "lake") != 0
        )
    ) {
        errno = ENOENT;
        return -1;
    }
    char target[PATH_MAX];
    int result = snprintf(
        target,
        sizeof(target),
        "%s/%s",
        directory,
        application
    );
    if (result < 0 || (size_t)result >= sizeof(target)) {
        errno = ENAMETOOLONG;
        return -1;
    }
    size_t length = (size_t)result;
    if (length > size) {
        length = size;
    }
    memcpy(buffer, target, length);
    return (ssize_t)length;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    if (
        is_proc_exe_path(path)
        && program_invocation_short_name != NULL
        && (
            strcmp(program_invocation_short_name, "lean") == 0
            || strcmp(program_invocation_short_name, "lake") == 0
        )
    ) {
        return supply_app_path(buffer, size);
    }
    static readlink_fn original = NULL;
    if (original == NULL) {
        original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (original == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return original(path, buffer, size);
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    if (
        is_proc_exe_path(path)
        && program_invocation_short_name != NULL
        && (
            strcmp(program_invocation_short_name, "lean") == 0
            || strcmp(program_invocation_short_name, "lake") == 0
        )
    ) {
        return supply_app_path(buffer, size);
    }
    static readlinkat_fn original = NULL;
    if (original == NULL) {
        original = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
    }
    if (original == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return original(directory, path, buffer, size);
}
