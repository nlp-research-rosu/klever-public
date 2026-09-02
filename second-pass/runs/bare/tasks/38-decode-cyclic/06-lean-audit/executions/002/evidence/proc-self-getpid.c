#define _GNU_SOURCE
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox virtualizes getpid() but exposes host-side process
 * directories through /proc. Lean 4.22 formats /proc/<getpid()>/exe when
 * implementing IO.appPath, so return the identifier named by /proc/self.
 */
pid_t getpid(void) {
  char buffer[64];
  ssize_t length = readlink("/proc/self", buffer, sizeof(buffer) - 1);
  if (length <= 0 || length >= (ssize_t)sizeof(buffer)) {
    return (pid_t)1;
  }
  buffer[length] = '\0';
  return (pid_t)strtol(buffer, NULL, 10);
}
