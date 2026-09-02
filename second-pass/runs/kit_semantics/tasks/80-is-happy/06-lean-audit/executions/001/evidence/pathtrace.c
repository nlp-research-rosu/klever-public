#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next_fn)(const char *, char *, size_t) = NULL;
  if (!next_fn) next_fn = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = next_fn(path, buf, size);
  int saved = errno;
  fprintf(stderr, "PATHTRACE readlink path=%s result=%zd errno=%d value=%.*s\n",
          path, result, saved, result > 0 ? (int)result : 0, buf);
  errno = saved;
  return result;
}

char *realpath(const char *path, char *resolved) {
  static char *(*next_fn)(const char *, char *) = NULL;
  if (!next_fn) next_fn = dlsym(RTLD_NEXT, "realpath");
  char *result = next_fn(path, resolved);
  int saved = errno;
  fprintf(stderr, "PATHTRACE realpath path=%s result=%s errno=%d\n",
          path, result ? result : "(null)", saved);
  errno = saved;
  return result;
}

char *getcwd(char *buf, size_t size) {
  static char *(*next_fn)(char *, size_t) = NULL;
  if (!next_fn) next_fn = dlsym(RTLD_NEXT, "getcwd");
  char *result = next_fn(buf, size);
  int saved = errno;
  fprintf(stderr, "PATHTRACE getcwd result=%s errno=%d\n",
          result ? result : "(null)", saved);
  errno = saved;
  return result;
}
