#define _GNU_SOURCE
#include <ctype.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * The managed audit PID namespace returns a getpid() value whose numeric
 * /proc/<pid> entry is not mounted. Lean 4.22 uses that spelling instead of
 * /proc/self/exe. Rewrite only the exact /proc/<digits>/exe lookup to the
 * kernel-equivalent self spelling; forward every other readlink unchanged.
 */
ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    const char prefix[] = "/proc/";
    const char suffix[] = "/exe";
    const char *p = path;
    int numeric_self_path = 0;
    if (p != NULL && strncmp(p, prefix, sizeof(prefix) - 1) == 0) {
        p += sizeof(prefix) - 1;
        const char *digits = p;
        while (isdigit((unsigned char)*p)) {
            ++p;
        }
        numeric_self_path = p > digits && strcmp(p, suffix) == 0;
    }
    const char *effective = numeric_self_path ? "/proc/self/exe" : path;
    return syscall(SYS_readlinkat, AT_FDCWD, effective, buf, bufsiz);
}
