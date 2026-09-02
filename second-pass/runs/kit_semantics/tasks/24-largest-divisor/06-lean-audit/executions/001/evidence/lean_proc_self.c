#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

static const char *normalized_proc_exe(const char *path) {
  if (path != NULL &&
      strncmp(path, "/proc/", 6) == 0 &&
      strcmp(path + strlen(path) - 4, "/exe") == 0) {
    return "/proc/self/exe";
  }
  return path;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) {
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  }
  return real_readlink(normalized_proc_exe(path), buf, size);
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);
  if (!real_readlinkat) {
    real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  }
  return real_readlinkat(dirfd, normalized_proc_exe(path), buf, size);
}
