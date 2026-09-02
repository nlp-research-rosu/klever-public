#define _GNU_SOURCE
#include <fcntl.h>
#include <stddef.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void) {
  char buffer[4096];
  int fd = (int)syscall(SYS_openat, AT_FDCWD, "/proc/self/status",
                        O_RDONLY | O_CLOEXEC, 0);
  if (fd >= 0) {
    ssize_t count = (ssize_t)syscall(SYS_read, fd, buffer,
                                     sizeof(buffer) - 1);
    syscall(SYS_close, fd);
    if (count > 0) {
      buffer[count] = '\0';
      const char *prefix = "Pid:";
      for (ssize_t index = 0; index + 4 < count; ++index) {
        if ((index == 0 || buffer[index - 1] == '\n') &&
            buffer[index] == prefix[0] &&
            buffer[index + 1] == prefix[1] &&
            buffer[index + 2] == prefix[2] &&
            buffer[index + 3] == prefix[3]) {
          return (pid_t)strtol(buffer + index + 4, NULL, 10);
        }
      }
    }
  }
  return (pid_t)syscall(SYS_getpid);
}
