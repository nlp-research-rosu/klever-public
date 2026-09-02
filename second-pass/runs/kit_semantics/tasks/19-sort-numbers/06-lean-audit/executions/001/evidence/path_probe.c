#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next)(const char *, char *, size_t);
  if (!next) next = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = next(path, buf, size);
  fprintf(stderr, "PROBE readlink(%s) = %zd errno=%d value=%.*s\n",
          path, result, errno, result > 0 ? (int)result : 0, buf);
  return result;
}

ssize_t readlinkat(int fd, const char *path, char *buf, size_t size) {
  static ssize_t (*next)(int, const char *, char *, size_t);
  if (!next) next = dlsym(RTLD_NEXT, "readlinkat");
  ssize_t result = next(fd, path, buf, size);
  fprintf(stderr, "PROBE readlinkat(%d,%s) = %zd errno=%d value=%.*s\n",
          fd, path, result, errno, result > 0 ? (int)result : 0, buf);
  return result;
}

char *realpath(const char *path, char *resolved) {
  static char *(*next)(const char *, char *);
  if (!next) next = dlsym(RTLD_NEXT, "realpath");
  char *result = next(path, resolved);
  fprintf(stderr, "PROBE realpath(%s) = %s errno=%d\n",
          path, result ? result : "(null)", errno);
  return result;
}

char *getcwd(char *buf, size_t size) {
  static char *(*next)(char *, size_t);
  if (!next) next = dlsym(RTLD_NEXT, "getcwd");
  char *result = next(buf, size);
  fprintf(stderr, "PROBE getcwd = %s errno=%d\n",
          result ? result : "(null)", errno);
  return result;
}
