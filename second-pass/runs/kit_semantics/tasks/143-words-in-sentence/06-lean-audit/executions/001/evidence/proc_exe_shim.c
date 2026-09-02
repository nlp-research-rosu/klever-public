#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/auxv.h>
#include <unistd.h>

/*
 * The managed audit sandbox exposes a PID namespace in which getpid() and
 * /proc disagree. Lean's IO.appPath reads /proc/<getpid>/exe, so repair only
 * that lookup from the kernel-provided executable name in AT_EXECFN.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    const char *prefix = "/proc/";
    size_t length = strlen(path);
    int is_proc_exe =
        strncmp(path, prefix, strlen(prefix)) == 0 &&
        length >= 4 &&
        strcmp(path + length - 4, "/exe") == 0;

    if (is_proc_exe) {
        const char *execfn = (const char *)getauxval(AT_EXECFN);
        if (execfn != NULL && execfn[0] != '\0') {
            char resolved[PATH_MAX];
            const char *answer = realpath(execfn, resolved);
            if (answer == NULL && execfn[0] == '/') {
                answer = execfn;
            }
            if (answer != NULL) {
                size_t answer_length = strlen(answer);
                size_t copied = answer_length < size ? answer_length : size;
                memcpy(buffer, answer, copied);
                return (ssize_t)copied;
            }
        }
    }

    if (real_readlink == NULL) {
        real_readlink = dlsym(RTLD_NEXT, "readlink");
        if (real_readlink == NULL) {
            errno = ENOSYS;
            return -1;
        }
    }
    return real_readlink(path, buffer, size);
}
