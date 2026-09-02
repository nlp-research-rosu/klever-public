#define _GNU_SOURCE

#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * Lean 4.22's Linux IO.appPath asks readlink("/proc/<getpid()>/exe").
 * In this audit sandbox, getpid() is namespace-local while /proc is mounted
 * from another namespace.  /proc/self/exe remains correct.  Redirect only
 * that exact path shape and leave all other readlink calls unchanged.
 */
ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t length = strlen(path);
    const char *effective = path;

    if (length > sizeof(prefix) - 1 + sizeof(suffix) - 1
        && strncmp(path, prefix, sizeof(prefix) - 1) == 0
        && strcmp(path + length - (sizeof(suffix) - 1), suffix) == 0) {
        effective = "/proc/self/exe";
    }

    return syscall(SYS_readlink, effective, buffer, size);
}
