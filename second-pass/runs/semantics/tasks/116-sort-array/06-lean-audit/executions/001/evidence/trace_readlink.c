#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (!real_readlink)
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  int saved = errno;
  fprintf(stderr, "TRACE readlink path=%s size=%zu result=%zd errno=%d\n",
          path, size, result, saved);
  errno = saved;
  return result;
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlinkat)(int, const char *, char *, size_t) = NULL;
  if (!real_readlinkat)
    real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  ssize_t result = real_readlinkat(dirfd, path, buf, size);
  int saved = errno;
  fprintf(stderr,
          "TRACE readlinkat dirfd=%d path=%s size=%zu result=%zd errno=%d\n",
          dirfd, path, size, result, saved);
  errno = saved;
  return result;
}
