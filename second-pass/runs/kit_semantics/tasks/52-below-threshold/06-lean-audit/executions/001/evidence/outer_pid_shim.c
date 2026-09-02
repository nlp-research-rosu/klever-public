#define _GNU_SOURCE

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Audit-container compatibility shim.
 *
 * Lean 4.22 resolves its application path with /proc/<getpid()>/exe.  This
 * container exposes the host PID namespace in /proc but getpid() reports the
 * inner namespace PID.  Return the first (outermost) NSpid so Lean and Lake
 * can locate their otherwise immutable, pinned installation.
 */
pid_t getpid(void) {
    FILE *status = fopen("/proc/self/status", "r");
    char line[512];
    long outer = -1;

    if (status == NULL) {
        return (pid_t)-1;
    }
    while (fgets(line, sizeof(line), status) != NULL) {
        if (sscanf(line, "NSpid:%ld", &outer) == 1) {
            break;
        }
    }
    fclose(status);
    return (pid_t)outer;
}
