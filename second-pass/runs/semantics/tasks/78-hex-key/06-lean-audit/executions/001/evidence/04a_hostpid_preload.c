/*
 * The managed audit shell has a PID namespace whose /proc mount belongs to
 * the parent namespace. Lean 4.22 calls getpid() and then reads
 * /proc/<pid>/exe, so it cannot locate itself here. Return the parent-visible
 * Pid from /proc/self/status; this changes no candidate or provenance input.
 */
#define _GNU_SOURCE
#include <fcntl.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void) {
    char buffer[4096];
    const char prefix[] = "Pid:\t";
    int descriptor = open("/proc/self/status", O_RDONLY | O_CLOEXEC);
    if (descriptor < 0) {
        return (pid_t)-1;
    }
    ssize_t count = read(descriptor, buffer, sizeof(buffer) - 1);
    close(descriptor);
    if (count <= 0) {
        return (pid_t)-1;
    }
    buffer[count] = '\0';
    char *line = buffer;
    while (line < buffer + count) {
        if (strncmp(line, prefix, sizeof(prefix) - 1) == 0) {
            return (pid_t)strtol(line + sizeof(prefix) - 1, NULL, 10);
        }
        char *newline = strchr(line, '\n');
        if (newline == NULL) {
            break;
        }
        line = newline + 1;
    }
    return (pid_t)-1;
}
