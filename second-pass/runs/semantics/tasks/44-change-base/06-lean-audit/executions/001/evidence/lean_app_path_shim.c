#define _GNU_SOURCE
#include <sys/types.h>
#include <unistd.h>

/*
 * Lean 4.22's Linux IO.appPath constructs /proc/<getpid()>/exe.  In this
 * audit sandbox getpid() returns the inner namespace PID, while /proc is
 * mounted in the outer namespace.  /proc/self is still correct.  Return its
 * numeric target so Lean resolves exactly its running executable.
 */
pid_t getpid(void) {
    char target[64];
    ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
    pid_t value = 0;
    ssize_t index;
    if (length <= 0) {
        return (pid_t)-1;
    }
    target[length] = '\0';
    for (index = 0; index < length; ++index) {
        if (target[index] < '0' || target[index] > '9') {
            return (pid_t)-1;
        }
        value = (pid_t)(value * 10 + (target[index] - '0'));
    }
    return value;
}
