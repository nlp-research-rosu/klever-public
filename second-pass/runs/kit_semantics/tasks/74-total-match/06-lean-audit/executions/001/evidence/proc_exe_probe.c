#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
    char path[PATH_MAX];
    char target[PATH_MAX];
    pid_t pid = getpid();
    int n = snprintf(path, sizeof(path), "/proc/%ld/exe", (long)pid);
    if (n < 0 || (size_t)n >= sizeof(path)) {
        return 2;
    }
    ssize_t self_count = readlink("/proc/self/exe", target, sizeof(target) - 1);
    if (self_count >= 0) {
        target[self_count] = '\0';
    }
    printf("getpid=%ld\n", (long)pid);
    printf("self_readlink_count=%ld errno=%d target=%s\n",
           (long)self_count, errno, self_count >= 0 ? target : "");
    errno = 0;
    ssize_t pid_count = readlink(path, target, sizeof(target) - 1);
    if (pid_count >= 0) {
        target[pid_count] = '\0';
    }
    printf("pid_path=%s\n", path);
    printf("pid_readlink_count=%ld errno=%d target=%s\n",
           (long)pid_count, errno, pid_count >= 0 ? target : "");
    return 0;
}
