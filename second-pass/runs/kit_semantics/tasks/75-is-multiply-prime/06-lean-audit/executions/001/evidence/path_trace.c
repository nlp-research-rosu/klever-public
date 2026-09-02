#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next_readlink)(const char *, char *, size_t);
  if (!next_readlink) next_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = next_readlink(path, buf, size);
  int saved_errno = errno;
  fprintf(stderr, "TRACE readlink(%s)=%zd errno=%d", path, result, saved_errno);
  if (result >= 0) fprintf(stderr, " value=%.*s", (int)result, buf);
  fputc('\n', stderr);
  errno = saved_errno;
  return result;
}

char *realpath(const char *path, char *resolved) {
  static char *(*next_realpath)(const char *, char *);
  if (!next_realpath) next_realpath = dlsym(RTLD_NEXT, "realpath");
  char *result = next_realpath(path, resolved);
  int saved_errno = errno;
  fprintf(stderr, "TRACE realpath(%s)=%s errno=%d\n", path,
          result ? result : "NULL", saved_errno);
  errno = saved_errno;
  return result;
}

char *getcwd(char *buf, size_t size) {
  static char *(*next_getcwd)(char *, size_t);
  if (!next_getcwd) next_getcwd = dlsym(RTLD_NEXT, "getcwd");
  char *result = next_getcwd(buf, size);
  int saved_errno = errno;
  fprintf(stderr, "TRACE getcwd=%s errno=%d\n", result ? result : "NULL",
          saved_errno);
  errno = saved_errno;
  return result;
}
