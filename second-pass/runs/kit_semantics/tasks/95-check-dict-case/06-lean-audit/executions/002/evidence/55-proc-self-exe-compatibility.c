#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn real_readlink;
  if (!real_readlink) real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  int saved_errno = errno;
  if (result < 0 && (saved_errno == ENOENT || saved_errno == EACCES) &&
      strncmp(path, "/proc/", 6) == 0 &&
      strcmp(path + strlen(path) - 4, "/exe") == 0) {
    result = real_readlink("/proc/self/exe", buf, size);
    saved_errno = errno;
    fprintf(stderr, "TRACE fallback=/proc/self/exe result=%zd errno=%d\n",
            result, saved_errno);
  }
  fprintf(stderr, "TRACE readlink path=%s result=%zd errno=%d\n", path, result, saved_errno);
  errno = saved_errno;
  return result;
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t size) {
  static readlinkat_fn real_readlinkat;
  if (!real_readlinkat) real_readlinkat = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
  ssize_t result = real_readlinkat(dirfd, path, buf, size);
  int saved_errno = errno;
  fprintf(stderr, "TRACE readlinkat path=%s result=%zd errno=%d\n", path, result, saved_errno);
  errno = saved_errno;
  return result;
}
