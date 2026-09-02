#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn real_readlink;
  if (real_readlink == NULL) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }

  char current_exe[64];
  int length = snprintf(
      current_exe, sizeof(current_exe), "/proc/%ld/exe", (long)getpid());
  if (length > 0 && (size_t)length < sizeof(current_exe)
      && strcmp(path, current_exe) == 0) {
    path = "/proc/self/exe";
  }
  return real_readlink(path, buffer, size);
}
