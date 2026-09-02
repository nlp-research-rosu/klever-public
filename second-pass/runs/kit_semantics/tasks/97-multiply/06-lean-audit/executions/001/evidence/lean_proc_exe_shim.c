#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_short_name;

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_exe_lookup(const char *path) {
    size_t length = strlen(path);
    return strncmp(path, "/proc/", 6) == 0
        && length >= 10
        && strcmp(path + length - 4, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    }
    if (is_proc_exe_lookup(path)) {
        const char *toolchain =
            "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/";
        const char *name = program_invocation_short_name;
        if (name != NULL && (
            strcmp(name, "lean") == 0
            || strcmp(name, "lake") == 0
            || strcmp(name, "leanc") == 0
        )) {
            char target[256];
            size_t prefix_length = strlen(toolchain);
            size_t name_length = strlen(name);
            size_t length = prefix_length + name_length;
            if (length > sizeof(target) || length > size) {
                errno = ENAMETOOLONG;
                return -1;
            }
            memcpy(target, toolchain, prefix_length);
            memcpy(target + prefix_length, name, name_length);
            memcpy(buffer, target, length);
            return (ssize_t)length;
        }
    }
    return real_readlink(path, buffer, size);
}
