#define _GNU_SOURCE

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <unistd.h>

/*
 * Lean 4.22's IO.appPath reads /proc/<getpid()>/exe.  In this audit sandbox,
 * getpid() is PID-namespace-relative while /proc is host-relative.  Resolve
 * the host PID from /proc/self and expose it only to audited child commands.
 */
static pid_t audit_host_pid;

static void audit_init_host_pid(void) {
    char buffer[64];
    char *end = NULL;
    long parsed;
    ssize_t length;

    if (audit_host_pid != 0) {
        return;
    }
    length = readlink("/proc/self", buffer, sizeof(buffer) - 1);
    if (length <= 0 || length >= (ssize_t)sizeof(buffer)) {
        return;
    }
    buffer[length] = '\0';
    errno = 0;
    parsed = strtol(buffer, &end, 10);
    if (
        errno == 0
        && end != buffer
        && *end == '\0'
        && parsed > 0
        && parsed <= INT_MAX
    ) {
        audit_host_pid = (pid_t)parsed;
    }
}

__attribute__((constructor))
static void audit_host_pid_constructor(void) {
    audit_init_host_pid();
}

pid_t getpid(void) {
    audit_init_host_pid();
    return audit_host_pid;
}
