#define _GNU_SOURCE

#include <fcntl.h>
#include <stddef.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox's PID namespace and mounted /proc disagree. Lean 4.22
 * resolves its executable through /proc/<getpid()>/exe, so return the first
 * (host) NSpid value exposed by /proc/self/status.
 */
pid_t getpid(void) {
    char buffer[8192];
    const char key[] = "NSpid:";
    int descriptor = open("/proc/self/status", O_RDONLY | O_CLOEXEC);
    if (descriptor >= 0) {
        ssize_t length = read(descriptor, buffer, sizeof(buffer) - 1);
        close(descriptor);
        if (length > 0) {
            buffer[length] = '\0';
            for (ssize_t index = 0; index + (ssize_t)sizeof(key) < length;
                 ++index) {
                size_t offset = 0;
                while (offset < sizeof(key) - 1
                       && buffer[index + (ssize_t)offset] == key[offset]) {
                    ++offset;
                }
                if (offset == sizeof(key) - 1) {
                    ssize_t cursor = index + (ssize_t)offset;
                    while (cursor < length
                           && (buffer[cursor] == ' '
                               || buffer[cursor] == '\t')) {
                        ++cursor;
                    }
                    pid_t host_pid = 0;
                    while (cursor < length
                           && buffer[cursor] >= '0'
                           && buffer[cursor] <= '9') {
                        host_pid =
                            host_pid * 10 + (pid_t)(buffer[cursor] - '0');
                        ++cursor;
                    }
                    if (host_pid > 0) {
                        return host_pid;
                    }
                }
            }
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
