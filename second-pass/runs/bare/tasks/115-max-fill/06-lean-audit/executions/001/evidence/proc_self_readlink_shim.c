#define _GNU_SOURCE
#include <ctype.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    const size_t length = strlen(path);
    int is_pid_exe = (
        length > sizeof(prefix) - 1 + sizeof(suffix) - 1
        && strncmp(path, prefix, sizeof(prefix) - 1) == 0
        && strcmp(path + length - (sizeof(suffix) - 1), suffix) == 0
    );
    if (is_pid_exe) {
        const size_t first = sizeof(prefix) - 1;
        const size_t last = length - (sizeof(suffix) - 1);
        for (size_t index = first; index < last; ++index) {
            if (!isdigit((unsigned char)path[index])) {
                is_pid_exe = 0;
                break;
            }
        }
    }
    const char *resolved = is_pid_exe ? "/proc/self/exe" : path;
    return syscall(SYS_readlink, resolved, buffer, size);
}
