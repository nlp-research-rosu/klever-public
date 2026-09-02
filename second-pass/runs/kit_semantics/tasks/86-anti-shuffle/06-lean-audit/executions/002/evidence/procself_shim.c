#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit container exposes a procfs from a different PID namespace.
 * Lean 4.22 discovers its executable with /proc/<getpid()>/exe, which is
 * absent here.  /proc/self/exe is the kernel-provided equivalent.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (real_readlink == NULL) {
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  }
  const size_t length = strlen(path);
  if (strncmp(path, "/proc/", 6) == 0 && length >= 10 &&
      strcmp(path + length - 4, "/exe") == 0) {
    path = "/proc/self/exe";
  }
  return real_readlink(path, buffer, size);
}
