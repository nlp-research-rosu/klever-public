#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn real_readlink = NULL;
  if (real_readlink == NULL) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (real_readlink == NULL) {
      errno = ENOSYS;
      return -1;
    }
  }

  char expected[64];
  int length = snprintf(expected, sizeof(expected), "/proc/%ld/exe",
                        (long)getpid());
  if (length > 0 && (size_t)length < sizeof(expected) &&
      strcmp(path, expected) == 0) {
    return real_readlink("/proc/self/exe", buffer, size);
  }
  return real_readlink(path, buffer, size);
}
