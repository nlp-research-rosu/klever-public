#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn real_readlink;
  if (!real_readlink) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }
  ssize_t result = real_readlink(path, buffer, size);
  int saved_errno = errno;
  if (result < 0
      && strncmp(path, "/proc/", 6) == 0
      && strcmp(path + strlen(path) - 4, "/exe") == 0) {
    result = real_readlink("/proc/self/exe", buffer, size);
    saved_errno = errno;
  }
  fprintf(stderr, "[readlink] path=%s size=%zu result=%zd errno=%d value=%.*s\n",
          path, size, result, saved_errno,
          result > 0 ? (int)result : 0, result > 0 ? buffer : "");
  errno = saved_errno;
  return result;
}
