#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
  char link[4096];
  char out[4096] = {0};
  snprintf(link, sizeof(link), "/proc/%d/exe", getpid());
  ssize_t n = readlink(link, out, sizeof(out));
  printf("pid=%d link=%s n=%zd errno=%d (%s) out=%s\n",
         getpid(), link, n, errno, strerror(errno), out);
  memset(out, 0, sizeof(out));
  errno = 0;
  n = readlink("/proc/self/exe", out, sizeof(out));
  printf("self_link=/proc/self/exe n=%zd errno=%d (%s) out=%s\n",
         n, errno, strerror(errno), out);
  return n < 0;
}
