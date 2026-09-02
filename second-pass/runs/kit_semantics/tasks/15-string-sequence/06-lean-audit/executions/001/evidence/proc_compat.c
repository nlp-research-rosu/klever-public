#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit runner exposes /proc/self/exe but not /proc/<getpid()>/exe.
 * Lean 4.22 uses the latter. Retry the equivalent self path only when that
 * exact process-executable lookup fails; all other readlink calls are intact.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) {
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  }
  ssize_t result = real_readlink(path, buf, size);
  size_t length = strlen(path);
  if (
      result < 0
      && strncmp(path, "/proc/", 6) == 0
      && length >= 10
      && strcmp(path + length - 4, "/exe") == 0
  ) {
    result = real_readlink("/proc/self/exe", buf, size);
  }
  return result;
}
