#define _GNU_SOURCE

#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_numeric_proc_exe(const char *path) {
  const char prefix[] = "/proc/";
  const char suffix[] = "/exe";
  const size_t prefix_len = sizeof(prefix) - 1;
  const size_t suffix_len = sizeof(suffix) - 1;
  size_t length;
  size_t index;

  if (path == NULL || strncmp(path, prefix, prefix_len) != 0) {
    return 0;
  }
  length = strlen(path);
  if (length <= prefix_len + suffix_len ||
      strcmp(path + length - suffix_len, suffix) != 0) {
    return 0;
  }
  for (index = prefix_len; index < length - suffix_len; ++index) {
    if (path[index] < '0' || path[index] > '9') {
      return 0;
    }
  }
  return 1;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn real_readlink = NULL;
  if (real_readlink == NULL) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }
  if (is_numeric_proc_exe(path)) {
    path = "/proc/self/exe";
  }
  return real_readlink(path, buffer, size);
}
