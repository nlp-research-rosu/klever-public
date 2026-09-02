#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox exposes a host-mounted /proc while getpid() reports the
 * inner namespace PID. Lean/libuv therefore asks for /proc/<inner-pid>/exe,
 * which does not exist. Preserve readlink semantics and redirect only that
 * exact Linux executable-self lookup to the namespace-safe /proc/self/exe.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (real_readlink == NULL) {
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  }

  const char *cursor = path;
  if (strncmp(cursor, "/proc/", 6) == 0) {
    cursor += 6;
    const char *digits = cursor;
    while (isdigit((unsigned char)*cursor)) {
      ++cursor;
    }
    if (
      cursor > digits
      && strcmp(cursor, "/exe") == 0
    ) {
      path = "/proc/self/exe";
    }
  }
  return real_readlink(path, buffer, size);
}
