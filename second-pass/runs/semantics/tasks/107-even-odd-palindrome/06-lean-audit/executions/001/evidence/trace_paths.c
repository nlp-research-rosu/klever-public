#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next_readlink)(const char *, char *, size_t);
  if (!next_readlink)
    next_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = next_readlink(path, buf, size);
  int saved_errno = errno;
  fprintf(stderr, "TRACE readlink(%s) = %zd errno=%d value=%.*s\n",
          path, result, saved_errno, result > 0 ? (int)result : 0, buf);
  errno = saved_errno;
  return result;
}

ssize_t readlinkat(int fd, const char *path, char *buf, size_t size) {
  static ssize_t (*next_readlinkat)(int, const char *, char *, size_t);
  if (!next_readlinkat)
    next_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  ssize_t result = next_readlinkat(fd, path, buf, size);
  int saved_errno = errno;
  fprintf(stderr, "TRACE readlinkat(%d,%s) = %zd errno=%d value=%.*s\n",
          fd, path, result, saved_errno, result > 0 ? (int)result : 0, buf);
  errno = saved_errno;
  return result;
}

char *realpath(const char *path, char *resolved) {
  static char *(*next_realpath)(const char *, char *);
  if (!next_realpath)
    next_realpath = dlsym(RTLD_NEXT, "realpath");
  char *result = next_realpath(path, resolved);
  int saved_errno = errno;
  fprintf(stderr, "TRACE realpath(%s) = %s errno=%d\n",
          path, result ? result : "(null)", saved_errno);
  errno = saved_errno;
  return result;
}
