#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

static int is_numeric_proc_exe(const char *path) {
  const char prefix[] = "/proc/";
  const char suffix[] = "/exe";
  size_t length;
  size_t index;

  if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
    return 0;
  }
  length = strlen(path);
  if (length <= (sizeof(prefix) - 1) + (sizeof(suffix) - 1)
      || strcmp(path + length - (sizeof(suffix) - 1), suffix) != 0) {
    return 0;
  }
  for (index = sizeof(prefix) - 1;
       index < length - (sizeof(suffix) - 1);
       ++index) {
    if (!isdigit((unsigned char)path[index])) {
      return 0;
    }
  }
  return 1;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static ssize_t (*next_readlink)(const char *, char *, size_t) = NULL;
  if (next_readlink == NULL) {
    next_readlink = dlsym(RTLD_NEXT, "readlink");
  }
  if (is_numeric_proc_exe(path)) {
    path = "/proc/self/exe";
  }
  return next_readlink(path, buffer, size);
}
