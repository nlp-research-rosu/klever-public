#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

/*
 * Compatibility for the audit sandbox's PID/proc namespace mismatch.
 * If a process cannot resolve /proc/<its reported pid>/exe, retry the
 * equivalent kernel-provided /proc/self/exe link. All other calls retain
 * their original result and errno.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (!real_readlink)
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  int saved = errno;
  size_t length = strlen(path);
  if (result < 0 && strncmp(path, "/proc/", 6) == 0 &&
      length >= 10 && strcmp(path + length - 4, "/exe") == 0) {
    result = real_readlink("/proc/self/exe", buf, size);
    saved = errno;
  }
  errno = saved;
  return result;
}
