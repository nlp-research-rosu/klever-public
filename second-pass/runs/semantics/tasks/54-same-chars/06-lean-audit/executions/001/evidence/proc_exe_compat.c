#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit runner exposes /proc from a different PID namespace. Lean 4.22
 * asks for /proc/<getpid()>/exe, which is absent, although /proc/self/exe is
 * valid. Redirect only that executable-discovery lookup.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  size_t length = strlen(path);
  if (
    length > 10
    && strncmp(path, "/proc/", 6) == 0
    && strcmp(path + length - 4, "/exe") == 0
  ) {
    return real_readlink("/proc/self/exe", buf, size);
  }
  return real_readlink(path, buf, size);
}
