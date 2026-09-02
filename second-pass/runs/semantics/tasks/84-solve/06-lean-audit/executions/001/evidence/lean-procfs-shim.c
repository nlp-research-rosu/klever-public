#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Audit-only environment shim. The sandbox exposes outer PIDs in /proc while
 * getpid() returns an inner namespace PID. Lean 4.22 uses
 * /proc/<getpid()>/exe. Return the outer Pid shown by /proc/self/status.
 */
pid_t getpid(void) {
    FILE *status = fopen("/proc/self/status", "r");
    if (status == NULL) {
        return (pid_t)-1;
    }

    char *line = NULL;
    size_t capacity = 0;
    pid_t outer_pid = (pid_t)-1;
    while (getline(&line, &capacity, status) != -1) {
        long value;
        if (sscanf(line, "Pid:\t%ld", &value) == 1) {
            outer_pid = (pid_t)value;
            break;
        }
    }
    free(line);
    fclose(status);
    return outer_pid;
}
