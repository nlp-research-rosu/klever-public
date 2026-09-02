#define _GNU_SOURCE
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * Codex's sandbox unshares PIDs without remounting procfs. Lean 4.22 asks
 * readlink("/proc/<getpid()>/exe"), where getpid() is namespace-relative,
 * but the mounted procfs exposes host-relative PIDs. Redirect only that
 * executable lookup to procfs's caller-aware /proc/self/exe.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    size_t length = strlen(path);
    int proc_executable =
        length > sizeof(prefix) - 1 + sizeof(suffix) - 1 &&
        strncmp(path, prefix, sizeof(prefix) - 1) == 0 &&
        strcmp(path + length - (sizeof(suffix) - 1), suffix) == 0;
    const char *resolved = proc_executable ? "/proc/self/exe" : path;
    return syscall(SYS_readlinkat, AT_FDCWD, resolved, buffer, size);
}
