#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc from a different PID namespace. Lean 4.22
 * asks for /proc/<getpid()>/exe, which is absent even though /proc/self/exe is
 * correct. Redirect only that failed lookup; all other readlink calls are
 * untouched.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next_readlink)(const char *, char *, size_t);
  if (!next_readlink)
    next_readlink = dlsym(RTLD_NEXT, "readlink");

  ssize_t result = next_readlink(path, buf, size);
  int saved_errno = errno;
  if (result == -1 && saved_errno == ENOENT) {
    char expected[64];
    int count = snprintf(expected, sizeof expected, "/proc/%ld/exe",
                         (long)getpid());
    if (count > 0 && (size_t)count < sizeof expected &&
        strcmp(path, expected) == 0) {
      result = next_readlink("/proc/self/exe", buf, size);
      saved_errno = errno;
    }
  }
  errno = saved_errno;
  return result;
}
