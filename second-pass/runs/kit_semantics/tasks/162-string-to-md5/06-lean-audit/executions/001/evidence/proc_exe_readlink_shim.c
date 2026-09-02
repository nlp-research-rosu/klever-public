#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
  static readlink_fn real_readlink = NULL;
  if (real_readlink == NULL)
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  if (path != NULL && strncmp(path, "/proc/", 6) == 0) {
    const char *suffix = strrchr(path, '/');
    if (suffix != NULL && strcmp(suffix, "/exe") == 0)
      return real_readlink("/proc/self/exe", buf, bufsiz);
  }
  return real_readlink(path, buf, bufsiz);
}
