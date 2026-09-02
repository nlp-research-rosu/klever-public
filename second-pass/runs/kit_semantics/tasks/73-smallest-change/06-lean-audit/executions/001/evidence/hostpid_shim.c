#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The managed sandbox creates a PID namespace but exposes the host /proc.
 * Lean 4.22's IO.appPath builds /proc/<getpid()>/exe, so its namespace PID
 * is absent from that procfs. Return the host PID exposed by /proc/self.
 */
pid_t getpid(void) {
  char target[64];
  ssize_t length = readlink("/proc/self", target, sizeof(target) - 1);
  if (length <= 0 || length >= (ssize_t)sizeof(target)) {
    return (pid_t)1;
  }
  target[length] = '\0';
  char *end = NULL;
  long value = strtol(target, &end, 10);
  if (end == target || *end != '\0' || value <= 0 || value > INT_MAX) {
    return (pid_t)1;
  }
  return (pid_t)value;
}
