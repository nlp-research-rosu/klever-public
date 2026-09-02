#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");

  char hidden_self[64];
  snprintf(hidden_self, sizeof(hidden_self), "/proc/%ld/exe", (long)getpid());
  if (path && strcmp(path, hidden_self) == 0)
    return real_readlink("/proc/self/exe", buf, size);
  return real_readlink(path, buf, size);
}
