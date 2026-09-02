#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_name;

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int self_exe_request(const char *path) {
    char expected[64];
    int length = snprintf(expected, sizeof(expected), "/proc/%ld/exe", (long)getpid());
    return length > 0 && (size_t)length < sizeof(expected) && strcmp(path, expected) == 0;
}

static char *invocation_path(void) {
    if (program_invocation_name == NULL || program_invocation_name[0] == '\0') {
        return NULL;
    }
    if (strchr(program_invocation_name, '/') != NULL) {
        return realpath(program_invocation_name, NULL);
    }
    const char *path = getenv("PATH");
    if (path == NULL) {
        return NULL;
    }
    char *copy = strdup(path);
    if (copy == NULL) {
        return NULL;
    }
    char *cursor = copy;
    char *directory;
    char *resolved = NULL;
    while ((directory = strsep(&cursor, ":")) != NULL) {
        if (directory[0] == '\0') {
            directory = ".";
        }
        size_t needed = strlen(directory) + strlen(program_invocation_name) + 2;
        char *candidate = malloc(needed);
        if (candidate == NULL) {
            break;
        }
        snprintf(candidate, needed, "%s/%s", directory, program_invocation_name);
        if (access(candidate, X_OK) == 0) {
            resolved = realpath(candidate, NULL);
            free(candidate);
            break;
        }
        free(candidate);
    }
    free(copy);
    return resolved;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn next_readlink;
    if (next_readlink == NULL) {
        next_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (self_exe_request(path)) {
        char *resolved = invocation_path();
        if (resolved != NULL) {
            size_t length = strlen(resolved);
            size_t copied = length < size ? length : size;
            memcpy(buffer, resolved, copied);
            free(resolved);
            return (ssize_t)copied;
        }
    }
    if (next_readlink == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return next_readlink(path, buffer, size);
}
