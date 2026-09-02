#define _GNU_SOURCE
/* Sandbox-only executable-path workaround; it does not alter Lean inputs. */
#include <dlfcn.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
typedef ssize_t (*readlinkat_fn)(int, const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn original;
  if (!original) original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  ssize_t result = original(path, buf, size);
  size_t path_length = path ? strlen(path) : 0;
  if (result < 0 && path_length >= 10 && strncmp(path, "/proc/", 6) == 0 &&
      strcmp(path + path_length - 4, "/exe") == 0) {
    result = original("/proc/self/exe", buf, size);
  }
  dprintf(2, "TRACE readlink path=%s result=%zd value=%.*s\n",
          path, result, result > 0 ? (int)result : 0, buf);
  return result;
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t size) {
  static readlinkat_fn original;
  if (!original) original = (readlinkat_fn)dlsym(RTLD_NEXT, "readlinkat");
  ssize_t result = original(dirfd, path, buf, size);
  dprintf(2, "TRACE readlinkat dirfd=%d path=%s result=%zd value=%.*s\n",
          dirfd, path, result, result > 0 ? (int)result : 0, buf);
  return result;
}
