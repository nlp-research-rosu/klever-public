#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn real_readlink;
  char namespace_path[64];

  if (real_readlink == NULL) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }
  (void)snprintf(
      namespace_path,
      sizeof(namespace_path),
      "/proc/%ld/exe",
      (long)getpid());
  if (strcmp(path, namespace_path) == 0) {
    return real_readlink("/proc/self/exe", buffer, size);
  }
  return real_readlink(path, buffer, size);
}
