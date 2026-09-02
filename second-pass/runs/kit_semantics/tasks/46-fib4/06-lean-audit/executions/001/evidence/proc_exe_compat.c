#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox creates a PID namespace without remounting /proc.
 * Lean asks for /proc/<namespace-pid>/exe, which therefore returns ENOENT.
 * Retry only that missing numeric process-executable lookup through the
 * kernel's process-relative /proc/self/exe alias.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  int saved = errno;
  if (result < 0 && saved == ENOENT && strncmp(path, "/proc/", 6) == 0) {
    const char *cursor = path + 6;
    if (isdigit((unsigned char)*cursor)) {
      while (isdigit((unsigned char)*cursor)) ++cursor;
      if (strcmp(cursor, "/exe") == 0) {
        result = real_readlink("/proc/self/exe", buf, size);
        saved = errno;
      }
    }
  }
  errno = saved;
  return result;
}
