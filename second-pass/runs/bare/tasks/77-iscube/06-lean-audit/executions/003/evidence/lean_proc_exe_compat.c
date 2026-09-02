#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * This audit runner exposes /proc in the host PID namespace while getpid()
 * returns the process's nested-namespace PID. Lean 4.22 constructs
 * /proc/<getpid()>/exe, so its application-path lookup fails. Redirect only
 * that exact readlink shape to the kernel-provided /proc/self/exe alias.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t length = strlen(path);
    int matches = length > sizeof(prefix) + sizeof(suffix) - 2
        && strncmp(path, prefix, sizeof(prefix) - 1) == 0
        && strcmp(path + length - (sizeof(suffix) - 1), suffix) == 0;
    const char *effective = matches ? "/proc/self/exe" : path;
    return syscall(SYS_readlinkat, AT_FDCWD, effective, buffer, size);
}
