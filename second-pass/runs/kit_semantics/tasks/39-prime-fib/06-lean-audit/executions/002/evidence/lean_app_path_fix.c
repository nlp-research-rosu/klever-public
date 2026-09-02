#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn real_readlink;
  if (!real_readlink)
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  size_t n = strlen(path);
  if (n > 10 && strncmp(path, "/proc/", 6) == 0 &&
      strcmp(path + n - 4, "/exe") == 0)
    path = "/proc/self/exe";
  return real_readlink(path, buf, size);
}
