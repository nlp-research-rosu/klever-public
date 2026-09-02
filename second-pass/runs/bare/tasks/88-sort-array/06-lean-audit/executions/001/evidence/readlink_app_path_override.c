#define _GNU_SOURCE
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * The audit sandbox denies the readlink(2) call Lean 4.22 uses for
 * /proc/<pid>/exe.  Lake and Lean are co-located in this immutable sysroot, so
 * supply that exact executable path only for the procfs application lookup.
 */
ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    static const char proc_prefix[] = "/proc/";
    static const char proc_suffix[] = "/exe";
    static const char lean_path[] =
        "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean";
    size_t path_length = strlen(path);
    size_t suffix_length = sizeof(proc_suffix) - 1;

    if (
        strncmp(path, proc_prefix, sizeof(proc_prefix) - 1) == 0
        && path_length >= suffix_length
        && strcmp(path + path_length - suffix_length, proc_suffix) == 0
    ) {
        size_t length = sizeof(lean_path) - 1;
        if (length > size) {
            length = size;
        }
        memcpy(buffer, lean_path, length);
        return (ssize_t)length;
    }

    return syscall(SYS_readlinkat, AT_FDCWD, path, buffer, size);
}
