#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn original;
  if (original == NULL) {
    original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }
  const size_t length = strlen(path);
  if (strncmp(path, "/proc/", 6) == 0 &&
      length >= 10 &&
      strcmp(path + length - 4, "/exe") == 0) {
    return original("/proc/self/exe", buffer, size);
  }
  return original(path, buffer, size);
}
