#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
    char proc_path[64];
    char target[PATH_MAX];
    snprintf(proc_path, sizeof(proc_path), "/proc/%d/exe", (int)getpid());
    ssize_t size = readlink(proc_path, target, sizeof(target) - 1);
    if (size < 0) {
        fprintf(stderr, "readlink(%s): errno=%d %s\n", proc_path, errno, strerror(errno));
        return 1;
    }
    target[size] = '\0';
    printf("%s -> %s\n", proc_path, target);
    return 0;
}
