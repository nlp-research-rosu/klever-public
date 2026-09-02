#define _GNU_SOURCE

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/* Lean 4.22 reads /proc/<getpid()>/exe, while this audit sandbox exposes
 * numeric /proc entries from the outer PID namespace. */
pid_t getpid(void) {
    char buffer[8192];
    int fd = open("/proc/self/status", O_RDONLY | O_CLOEXEC);
    if (fd >= 0) {
        ssize_t count = read(fd, buffer, sizeof(buffer) - 1);
        close(fd);
        if (count > 0) {
            buffer[count] = '\0';
            const char *cursor = buffer;
            while (cursor < buffer + count) {
                if (strncmp(cursor, "Pid:", 4) == 0) {
                    char *end = NULL;
                    long value = strtol(cursor + 4, &end, 10);
                    if (end != cursor + 4 && value > 0) {
                        return (pid_t)value;
                    }
                }
                const char *newline = strchr(cursor, '\n');
                if (newline == NULL) {
                    break;
                }
                cursor = newline + 1;
            }
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
