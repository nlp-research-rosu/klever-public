#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <libgen.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_name;

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_exe_query(const char *path) {
    size_t length = strlen(path);
    return strncmp(path, "/proc/", 6) == 0
        && length >= 4
        && strcmp(path + length - 4, "/exe") == 0;
}

static const char *current_executable(void) {
    const char *name = program_invocation_name;
    const char *base = strrchr(name, '/');
    base = base == NULL ? name : base + 1;
    if (strcmp(base, "lake") == 0) {
        return "/tmp/audit-work/lake-bin/lake";
    }
    if (strcmp(base, "lean") == 0) {
        return "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean";
    }
    if (strcmp(base, "leanc") == 0) {
        return "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/leanc";
    }
    return name;
}

ssize_t readlink(const char *path, char *buffer, size_t buffer_size) {
    static readlink_fn real_readlink = NULL;
    if (is_proc_exe_query(path)) {
        const char *executable = current_executable();
        size_t length = strlen(executable);
        if (length > buffer_size) {
            length = buffer_size;
        }
        memcpy(buffer, executable, length);
        return (ssize_t)length;
    }
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    return real_readlink(path, buffer, buffer_size);
}
