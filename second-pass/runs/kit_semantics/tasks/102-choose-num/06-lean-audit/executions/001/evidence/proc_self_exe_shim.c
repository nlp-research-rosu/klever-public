#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

static bool is_numeric_proc_exe(const char *path) {
  if (strncmp(path, "/proc/", 6) != 0) return false;
  const char *cursor = path + 6;
  if (*cursor < '0' || *cursor > '9') return false;
  while (*cursor >= '0' && *cursor <= '9') cursor++;
  return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  if (is_numeric_proc_exe(path)) path = "/proc/self/exe";
  return real_readlink(path, buf, bufsiz);
}
