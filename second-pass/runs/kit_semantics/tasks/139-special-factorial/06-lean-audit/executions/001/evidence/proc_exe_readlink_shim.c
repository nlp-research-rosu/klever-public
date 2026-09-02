#define _GNU_SOURCE

#include <ctype.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * This audit sandbox exposes /proc/self correctly but does not expose the
 * namespace-local numeric PID returned by getpid(). Lean 4.22 resolves its
 * executable as /proc/<getpid()>/exe, so redirect only that procfs shape to
 * /proc/self/exe. All other readlink calls pass straight to the kernel.
 */
static int is_proc_pid_exe(const char *path) {
    static const char prefix[] = "/proc/";
    const char *cursor;

    if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
        return 0;
    }
    cursor = path + sizeof(prefix) - 1;
    if (!isdigit((unsigned char)*cursor)) {
        return 0;
    }
    while (isdigit((unsigned char)*cursor)) {
        ++cursor;
    }
    return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    const char *effective = is_proc_pid_exe(path) ? "/proc/self/exe" : path;
    return syscall(SYS_readlink, effective, buffer, size);
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
    const char *effective = is_proc_pid_exe(path) ? "/proc/self/exe" : path;
    return syscall(SYS_readlinkat, directory, effective, buffer, size);
}
