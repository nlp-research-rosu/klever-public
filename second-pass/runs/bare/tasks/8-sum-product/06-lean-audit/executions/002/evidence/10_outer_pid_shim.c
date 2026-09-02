#define _GNU_SOURCE
#include <ctype.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void) {
  char buffer[4096];
  int fd = open("/proc/self/status", O_RDONLY | O_CLOEXEC);
  if (fd >= 0) {
    ssize_t count = read(fd, buffer, sizeof(buffer) - 1);
    close(fd);
    if (count > 0) {
      buffer[count] = '\0';
      const char *line = strstr(buffer, "Pid:");
      if (line != NULL) {
        line += 4;
        while (*line != '\0' && isspace((unsigned char)*line)) {
          ++line;
        }
        char *end = NULL;
        long value = strtol(line, &end, 10);
        if (end != line && value > 0) {
          return (pid_t)value;
        }
      }
    }
  }
  return (pid_t)syscall(SYS_getpid);
}
