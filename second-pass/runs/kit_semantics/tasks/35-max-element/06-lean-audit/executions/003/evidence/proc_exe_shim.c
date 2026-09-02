#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_short_name;

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static readlink_fn real_readlink = NULL;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    size_t length = strlen(path);
    if (strncmp(path, "/proc/", 6) != 0 || length < 10 ||
        strcmp(path + length - 4, "/exe") != 0) {
        return real_readlink(path, buf, bufsiz);
    }
    const char *name = program_invocation_short_name;
    if (name == NULL || strchr(name, '/') != NULL) {
        return real_readlink(path, buf, bufsiz);
    }
    char executable[PATH_MAX];
    int needed = snprintf(
        executable,
        sizeof(executable),
        "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/%s",
        name
    );
    if (needed < 0 || (size_t)needed >= sizeof(executable) ||
        access(executable, X_OK) != 0) {
        return real_readlink(path, buf, bufsiz);
    }
    size_t copy = (size_t)needed < bufsiz ? (size_t)needed : bufsiz;
    memcpy(buf, executable, copy);
    return (ssize_t)copy;
}
