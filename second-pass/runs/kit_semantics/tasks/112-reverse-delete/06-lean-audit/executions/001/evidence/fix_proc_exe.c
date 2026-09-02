#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_name;

static int is_proc_exe(const char *path) {
    if (strcmp(path, "/proc/self/exe") == 0) return 1;
    if (strncmp(path, "/proc/", 6) != 0) return 0;
    const char *cursor = path + 6;
    if (*cursor < '0' || *cursor > '9') return 0;
    while (*cursor >= '0' && *cursor <= '9') cursor++;
    return strcmp(cursor, "/exe") == 0;
}

static ssize_t invocation_path(char *buffer, size_t size) {
    const char *name = program_invocation_name;
    char resolved[PATH_MAX];
    if (name == NULL) {
        errno = ENOENT;
        return -1;
    }
    if (strchr(name, '/') != NULL) {
        if (realpath(name, resolved) == NULL) return -1;
    } else {
        const char *search = getenv("PATH");
        if (search == NULL) {
            errno = ENOENT;
            return -1;
        }
        char *paths = strdup(search);
        if (paths == NULL) return -1;
        char *state = NULL;
        char *directory = strtok_r(paths, ":", &state);
        int found = 0;
        while (directory != NULL) {
            char candidate[PATH_MAX];
            if (snprintf(candidate, sizeof(candidate), "%s/%s", directory, name)
                    < (int)sizeof(candidate)
                && access(candidate, X_OK) == 0
                && realpath(candidate, resolved) != NULL) {
                found = 1;
                break;
            }
            directory = strtok_r(NULL, ":", &state);
        }
        free(paths);
        if (!found) {
            errno = ENOENT;
            return -1;
        }
    }
    size_t length = strlen(resolved);
    size_t copied = length < size ? length : size;
    memcpy(buffer, resolved, copied);
    return (ssize_t)copied;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*original)(const char *, char *, size_t) = NULL;
    if (is_proc_exe(path)) return invocation_path(buffer, size);
    if (original == NULL) original = dlsym(RTLD_NEXT, "readlink");
    return original(path, buffer, size);
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    static ssize_t (*original)(int, const char *, char *, size_t) = NULL;
    if (path != NULL && path[0] == '/' && is_proc_exe(path)) {
        return invocation_path(buffer, size);
    }
    if (original == NULL) original = dlsym(RTLD_NEXT, "readlinkat");
    return original(directory, path, buffer, size);
}
