#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) {
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  }
  errno = 0;
  ssize_t result = real_readlink(path, buf, size);
  int saved = errno;
  fprintf(stderr, "TRACE readlink(%s) = %zd errno=%d value=%.*s\n",
          path, result, saved, result > 0 ? (int)result : 0, buf);
  errno = saved;
  return result;
}
