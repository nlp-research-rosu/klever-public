#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn next;
  if (!next) next = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  ssize_t result = next(path, buf, size);
  size_t pathLen = strlen(path);
  if (result < 0 && pathLen >= 10 && strncmp(path, "/proc/", 6) == 0 &&
      strcmp(path + pathLen - 4, "/exe") == 0) {
    result = next("/proc/self/exe", buf, size);
  }
  return result;
}
