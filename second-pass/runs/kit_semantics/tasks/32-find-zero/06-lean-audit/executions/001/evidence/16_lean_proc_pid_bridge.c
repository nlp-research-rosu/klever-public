/*
 * Audit-container compatibility shim.
 *
 * The container's getpid() reports the inner PID namespace, but /proc is the
 * outer namespace's procfs. Lean 4.22 uses /proc/<getpid()>/exe to locate its
 * application, so it cannot start. Return the host-visible PID reported by
 * /proc/self/status. This changes no Lean source, project source, or theorem.
 */
#define _GNU_SOURCE

#include <fcntl.h>
#include <stddef.h>
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void) {
    char buffer[4096];
    const char prefix[] = "Pid:";
    int fd = open("/proc/self/status", O_RDONLY | O_CLOEXEC);
    if (fd < 0) {
        return (pid_t)-1;
    }
    ssize_t count = read(fd, buffer, sizeof(buffer) - 1);
    close(fd);
    if (count <= 0) {
        return (pid_t)-1;
    }
    buffer[count] = '\0';
    for (ssize_t i = 0; i + (ssize_t)sizeof(prefix) < count; ++i) {
        if (
            (i == 0 || buffer[i - 1] == '\n')
            && buffer[i] == 'P'
            && buffer[i + 1] == 'i'
            && buffer[i + 2] == 'd'
            && buffer[i + 3] == ':'
        ) {
            ssize_t j = i + 4;
            while (j < count && (buffer[j] == ' ' || buffer[j] == '\t')) {
                ++j;
            }
            pid_t result = 0;
            while (j < count && buffer[j] >= '0' && buffer[j] <= '9') {
                result = (pid_t)(result * 10 + (buffer[j] - '0'));
                ++j;
            }
            if (result > 0) {
                return result;
            }
            break;
        }
    }
    return (pid_t)-1;
}
