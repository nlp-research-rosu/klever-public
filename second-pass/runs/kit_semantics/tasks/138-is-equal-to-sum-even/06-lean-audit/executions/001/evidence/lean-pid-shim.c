#define _GNU_SOURCE

#include <dirent.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The managed command sandbox creates a PID namespace without mounting a
 * matching procfs. Lean's IO.appPath uses /proc/<getpid()>/exe, so translate
 * the namespace-local PID to the visible outer PID recorded in NSpid.
 */
pid_t getpid(void) {
    const pid_t inner = (pid_t)syscall(SYS_getpid);
    DIR *proc = opendir("/proc");
    if (proc == NULL) {
        return inner;
    }

    pid_t best = inner;
    struct dirent *entry;
    while ((entry = readdir(proc)) != NULL) {
        char *end = NULL;
        errno = 0;
        long outer_long = strtol(entry->d_name, &end, 10);
        if (errno != 0 || end == entry->d_name || *end != '\0' ||
            outer_long <= 0 || outer_long > INT_MAX) {
            continue;
        }

        char status_path[PATH_MAX];
        int written = snprintf(status_path, sizeof(status_path),
                               "/proc/%ld/status", outer_long);
        if (written <= 0 || (size_t)written >= sizeof(status_path)) {
            continue;
        }
        FILE *status = fopen(status_path, "r");
        if (status == NULL) {
            continue;
        }

        char line[4096];
        while (fgets(line, sizeof(line), status) != NULL) {
            if (strncmp(line, "NSpid:", 6) != 0) {
                continue;
            }
            char *cursor = line + 6;
            long last = -1;
            while (*cursor != '\0') {
                char *number_end = NULL;
                long value = strtol(cursor, &number_end, 10);
                if (number_end == cursor) {
                    cursor++;
                } else {
                    last = value;
                    cursor = number_end;
                }
            }
            if (last == inner && outer_long > best) {
                best = (pid_t)outer_long;
            }
            break;
        }
        fclose(status);
    }
    closedir(proc);
    return best;
}
