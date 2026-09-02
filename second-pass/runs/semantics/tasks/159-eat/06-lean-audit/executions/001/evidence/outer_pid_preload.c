#define _GNU_SOURCE
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * The command sandbox creates a nested PID namespace but exposes the parent
 * namespace's /proc. Lean 4.22 asks /proc/<getpid()>/exe for IO.appPath, which
 * therefore misses. Return the outer "Pid:" recorded in /proc/self/status so
 * Lean can resolve its own immutable executable. This changes no project data.
 */
pid_t getpid(void) {
    FILE *stream = fopen("/proc/self/status", "r");
    char *line = NULL;
    size_t capacity = 0;
    long result = -1;

    if (stream == NULL) {
        return (pid_t)-1;
    }
    while (getline(&line, &capacity, stream) >= 0) {
        if (strncmp(line, "Pid:", 4) == 0) {
            result = strtol(line + 4, NULL, 10);
            break;
        }
    }
    free(line);
    fclose(stream);
    return (pid_t)result;
}
