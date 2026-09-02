#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_name;

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink = NULL;
    const char *proc_prefix = "/proc/";
    const char *exe_suffix = "/exe";
    size_t path_length = strlen(path);
    size_t prefix_length = strlen(proc_prefix);
    size_t suffix_length = strlen(exe_suffix);
    int is_proc_exe =
        path_length > prefix_length + suffix_length &&
        strncmp(path, proc_prefix, prefix_length) == 0 &&
        strcmp(path + path_length - suffix_length, exe_suffix) == 0;

    if (is_proc_exe && program_invocation_name != NULL &&
        program_invocation_name[0] == '/') {
        size_t length = strlen(program_invocation_name);
        if (length > size) {
            length = size;
        }
        memcpy(buffer, program_invocation_name, length);
        return (ssize_t)length;
    }

    if (real_readlink == NULL) {
        real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    return real_readlink(path, buffer, size);
}
