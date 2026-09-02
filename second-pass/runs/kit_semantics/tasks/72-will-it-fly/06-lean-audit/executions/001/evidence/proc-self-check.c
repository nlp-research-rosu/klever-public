#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
  char path[128];
  char target[4096];
  snprintf(path, sizeof(path), "/proc/%d/exe", (int)getpid());
  ssize_t size = readlink(path, target, sizeof(target) - 1);
  if (size < 0) {
    fprintf(stderr, "readlink(%s): %s\n", path, strerror(errno));
    return 1;
  }
  target[size] = '\0';
  printf("pid=%d path=%s target=%s\n", (int)getpid(), path, target);
  return 0;
}
