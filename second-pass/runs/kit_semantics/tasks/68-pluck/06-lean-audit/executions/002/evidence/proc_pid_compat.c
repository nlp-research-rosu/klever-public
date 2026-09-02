#define _GNU_SOURCE

#include <ctype.h>
#include <stddef.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Lean 4.22 resolves its executable through /proc/<getpid()>/exe.
 * In this audit container, getpid() returns the inner namespace PID while the
 * mounted /proc exposes numeric entries in the outer namespace.  /proc/self
 * still resolves to the visible outer PID.  Return that PID so Lean's lookup
 * addresses the same process through the mounted procfs.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    if (length > 0) {
        long value = 0;
        target[length] = '\0';
        for (ssize_t index = 0; index < length; ++index) {
            if (!isdigit((unsigned char)target[index])) {
                value = 0;
                break;
            }
            value = value * 10 + (target[index] - '0');
        }
        if (value > 0) {
            return (pid_t)value;
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
