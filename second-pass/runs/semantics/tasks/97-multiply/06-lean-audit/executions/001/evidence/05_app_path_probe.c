#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    char name[128];
    char target[4096] = {0};
    int written = snprintf(name, sizeof(name), "/proc/%d/exe", getpid());
    ssize_t count = readlink(name, target, sizeof(target) - 1);
    printf("pid=%d name=%s snprintf=%d readlink=%zd errno=%d (%s) target=%s\n",
           getpid(), name, written, count, errno, strerror(errno), target);
    return count < 0;
}
