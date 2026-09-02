#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  int saved = errno;
  dprintf(2, "TRACE readlink(%s, size=%zu) -> %zd errno=%d", path, size, result, saved);
  if (result >= 0) dprintf(2, " value=%.*s", (int)result, buf);
  dprintf(2, "\n");
  errno = saved;
  return result;
}
