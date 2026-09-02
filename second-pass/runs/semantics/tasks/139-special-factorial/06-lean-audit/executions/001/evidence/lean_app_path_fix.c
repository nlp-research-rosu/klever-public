#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

static int is_proc_exe_path(const char *path) {
  size_t length;
  if (path == NULL || strncmp(path, "/proc/", 6) != 0) return 0;
  length = strlen(path);
  return length >= 10 && strcmp(path + length - 4, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*original)(const char *, char *, size_t);
  if (!original) original = dlsym(RTLD_NEXT, "readlink");
  return original(is_proc_exe_path(path) ? "/proc/self/exe" : path, buf, size);
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t size) {
  static ssize_t (*original)(int, const char *, char *, size_t);
  if (!original) original = dlsym(RTLD_NEXT, "readlinkat");
  if (is_proc_exe_path(path)) {
    return readlink("/proc/self/exe", buf, size);
  }
  return original(dirfd, path, buf, size);
}
