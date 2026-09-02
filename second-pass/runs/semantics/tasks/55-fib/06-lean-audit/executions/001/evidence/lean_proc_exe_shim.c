#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static readlink_fn real_readlink;
  if (real_readlink == NULL) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }

  const char *prefix = "/proc/";
  const char *cursor = path;
  if (strncmp(cursor, prefix, strlen(prefix)) == 0) {
    cursor += strlen(prefix);
    const char *digits = cursor;
    while (*cursor >= '0' && *cursor <= '9') {
      cursor++;
    }
    if (cursor != digits && strcmp(cursor, "/exe") == 0) {
      path = "/proc/self/exe";
    }
  }
  return real_readlink(path, buffer, size);
}
