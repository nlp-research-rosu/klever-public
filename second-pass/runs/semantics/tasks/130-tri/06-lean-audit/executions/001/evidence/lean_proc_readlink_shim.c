#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_function)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_function original_readlink;
  if (original_readlink == NULL) {
    original_readlink = (readlink_function)dlsym(RTLD_NEXT, "readlink");
  }

  ssize_t result = original_readlink(path, buffer, size);
  size_t length = strlen(path);
  if (result < 0 && length >= 10 && strncmp(path, "/proc/", 6) == 0 &&
      strcmp(path + length - 4, "/exe") == 0) {
    return original_readlink("/proc/self/exe", buffer, size);
  }
  return result;
}
