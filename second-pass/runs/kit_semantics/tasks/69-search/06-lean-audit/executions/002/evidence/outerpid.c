#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

/*
 * The audit sandbox unshares PID but exposes the parent /proc mount. Lean's
 * runtime calls getpid() and then /proc/<pid>/exe, which otherwise names a PID
 * absent from that mount. Return the /proc-visible PID, obtained from the
 * special /proc/self symlink, so the pinned unmodified Lean binary can locate
 * itself. This shim changes no Lean source or project input.
 */
pid_t getpid(void) {
    char buffer[64];
    ssize_t length = readlink("/proc/self", buffer, sizeof(buffer) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(buffer)) {
        return (pid_t)-1;
    }
    buffer[length] = '\0';
    return (pid_t)strtol(buffer, NULL, 10);
}
