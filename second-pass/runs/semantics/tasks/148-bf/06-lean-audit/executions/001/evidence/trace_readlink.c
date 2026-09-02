#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn real_readlink;
  if (!real_readlink) real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  int saved = errno;
  fprintf(stderr, "TRACE readlink(%s,%zu)=%zd errno=%d value=%.*s\n",
          path, size, result, saved, result > 0 ? (int)result : 0, buf);
  errno = saved;
  return result;
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t size) {
  static readlinkat_fn real_readlinkat;
  if (!real_readlinkat)
    real_readlinkat = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
  ssize_t result = real_readlinkat(dirfd, path, buf, size);
  int saved = errno;
  fprintf(stderr, "TRACE readlinkat(%d,%s,%zu)=%zd errno=%d value=%.*s\n",
          dirfd, path, size, result, saved, result > 0 ? (int)result : 0, buf);
  errno = saved;
  return result;
}
