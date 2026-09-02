#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn real_readlink;
  if (!real_readlink) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }
  if (path && strncmp(path, "/proc/", 6) == 0) {
    const char *suffix = strrchr(path, '/');
    if (suffix && strcmp(suffix, "/exe") == 0) {
      return real_readlink("/proc/self/exe", buffer, size);
    }
  }
  return real_readlink(path, buffer, size);
}
