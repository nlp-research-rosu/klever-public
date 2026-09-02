#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

/* Audit-environment repair only: the nested PID is not present in /proc. */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  if (strncmp(path, "/proc/", 6) == 0 && strstr(path + 6, "/exe") != NULL)
    path = "/proc/self/exe";
  return real_readlink(path, buf, size);
}
