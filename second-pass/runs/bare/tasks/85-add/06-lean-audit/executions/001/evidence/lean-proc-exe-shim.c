#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_short_name;

static int is_proc_pid_exe(const char *path) {
    const char *cursor;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
        return 0;
    }
    cursor = path + 6;
    if (*cursor < '0' || *cursor > '9') {
        return 0;
    }
    while (*cursor >= '0' && *cursor <= '9') {
        cursor++;
    }
    return strcmp(cursor, "/exe") == 0;
}

static int executable_from_path(char output[PATH_MAX]) {
    const char *name = program_invocation_short_name;
    const char *path_env = getenv("PATH");
    char *search;
    char *save = NULL;
    char *directory;

    if (name == NULL || *name == '\0' || path_env == NULL) {
        return -1;
    }
    search = strdup(path_env);
    if (search == NULL) {
        return -1;
    }
    for (directory = strtok_r(search, ":", &save);
         directory != NULL;
         directory = strtok_r(NULL, ":", &save)) {
        char candidate[PATH_MAX];
        if (snprintf(
                candidate,
                sizeof(candidate),
                "%s/%s",
                *directory == '\0' ? "." : directory,
                name
            ) >= (int)sizeof(candidate)) {
            continue;
        }
        if (access(candidate, X_OK) == 0 && realpath(candidate, output) != NULL) {
            free(search);
            return 0;
        }
    }
    free(search);
    return -1;
}

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static ssize_t (*real_readlink)(
        const char *restrict,
        char *restrict,
        size_t
    ) = NULL;

    if (is_proc_pid_exe(path)) {
        char executable[PATH_MAX];
        size_t length;
        if (executable_from_path(executable) == 0) {
            length = strlen(executable);
            if (length > size) {
                length = size;
            }
            memcpy(buffer, executable, length);
            return (ssize_t)length;
        }
    }
    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    return real_readlink(path, buffer, size);
}
