#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/*
 * Audit-container compatibility shim. Lean asks for /proc/<pid>/exe, while
 * this PID namespace exposes only /proc/self/exe. No other readlink is changed.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  const char *suffix = strrchr(path, '/');
  if (result < 0 && strncmp(path, "/proc/", 6) == 0 &&
      suffix && strcmp(suffix, "/exe") == 0) {
    result = real_readlink("/proc/self/exe", buf, size);
  }
  return result;
}
