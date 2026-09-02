#define _GNU_SOURCE

#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

static int read_small_file(const char *path, char *buffer, size_t capacity) {
    int fd = open(path, O_RDONLY | O_CLOEXEC);
    if (fd < 0) {
        return -1;
    }
    ssize_t count = read(fd, buffer, capacity - 1);
    close(fd);
    if (count < 0) {
        return -1;
    }
    buffer[count] = '\0';
    return (int)count;
}

pid_t getpid(void) {
    char comm[64];
    if (read_small_file("/proc/self/comm", comm, sizeof(comm)) > 0
        && (strcmp(comm, "lean\n") == 0
            || strcmp(comm, "lake\n") == 0)) {
        char status[4096];
        if (read_small_file("/proc/self/status", status, sizeof(status)) > 0) {
            const char *pid_line = strstr(status, "\nPid:\t");
            if (pid_line != NULL) {
                pid_line += strlen("\nPid:\t");
                long value = 0;
                while (*pid_line >= '0' && *pid_line <= '9') {
                    value = value * 10 + (*pid_line - '0');
                    ++pid_line;
                }
                if (value > 0) {
                    return (pid_t)value;
                }
            }
        }
    }
    return (pid_t)syscall(SYS_getpid);
}
