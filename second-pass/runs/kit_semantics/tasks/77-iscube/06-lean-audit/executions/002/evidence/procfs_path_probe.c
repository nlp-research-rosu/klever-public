#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

static void probe(const char *path) {
  char buffer[PATH_MAX];
  errno = 0;
  ssize_t count = readlink(path, buffer, sizeof(buffer) - 1);
  if (count < 0) {
    printf("%s: readlink failed: errno=%d (%s)\n", path, errno, strerror(errno));
  } else {
    buffer[count] = '\0';
    printf("%s: %s\n", path, buffer);
  }
}

int main(void) {
  char pid_path[64];
  snprintf(pid_path, sizeof(pid_path), "/proc/%ld/exe", (long)getpid());
  probe("/proc/self/exe");
  probe(pid_path);
  return 0;
}
