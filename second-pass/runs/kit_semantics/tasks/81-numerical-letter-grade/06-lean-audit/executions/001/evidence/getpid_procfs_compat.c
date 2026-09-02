#define _GNU_SOURCE
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

/*
 * The audit sandbox uses a PID namespace while exposing a procfs mounted from
 * its parent namespace. Lean 4.22 resolves its executable through
 * /proc/<getpid()>/exe, so provide the procfs-visible PID from
 * /proc/self/status.
 */
pid_t getpid(void) {
    FILE *status = fopen("/proc/self/status", "r");
    char *line = NULL;
    size_t capacity = 0;
    pid_t visible_pid = -1;
    if (status != NULL) {
        while (getline(&line, &capacity, status) != -1) {
            if (sscanf(line, "Pid:\t%d", &visible_pid) == 1) {
                break;
            }
        }
        fclose(status);
    }
    free(line);
    if (visible_pid <= 0) {
        abort();
    }
    return visible_pid;
}
