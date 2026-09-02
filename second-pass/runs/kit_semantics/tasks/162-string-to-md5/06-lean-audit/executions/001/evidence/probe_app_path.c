#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
  char link[4096];
  char target[4096] = {0};
  snprintf(link, sizeof(link), "/proc/%d/exe", getpid());
  ssize_t n = readlink(link, target, sizeof(target) - 1);
  printf("path=%s n=%zd errno=%d (%s) target=%s\n",
         link, n, errno, strerror(errno), target);
  return n < 0;
}
