#define _GNU_SOURCE
#include <limits.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * Diagnostic infrastructure workaround used for the fresh preflight only.
 * The managed PID namespace exposes /proc/self correctly but not
 * /proc/<namespace-pid>. Lean 4.22's IO.appPath uses getpid() followed by
 * /proc/<pid>/exe. Return the procfs-visible PID from /proc/self.
 */
pid_t getpid(void) {
  char buffer[64];
  ssize_t size = readlink("/proc/self", buffer, sizeof(buffer) - 1);
  if (size > 0 && size < (ssize_t)sizeof(buffer)) {
    buffer[size] = '\0';
    char *end = NULL;
    long value = strtol(buffer, &end, 10);
    if (end != buffer && *end == '\0' && value > 0 && value <= INT_MAX) {
      return (pid_t)value;
    }
  }
  return (pid_t)syscall(SYS_getpid);
}
