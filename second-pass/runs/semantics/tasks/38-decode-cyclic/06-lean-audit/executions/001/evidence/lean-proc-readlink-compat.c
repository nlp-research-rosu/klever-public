#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit command sandbox gives a process a PID-namespace getpid(), while
 * /proc is mounted from a different namespace. Lean 4.22 asks for
 * /proc/<getpid()>/exe and receives ENOENT. Fall back to the equivalent
 * /proc/self/exe link only for that exact failure shape.
 */
typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn real_readlink;
  if (!real_readlink)
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, size);
  if (result < 0 && errno == ENOENT) {
    size_t length = strlen(path);
    if (length >= 10 && strncmp(path, "/proc/", 6) == 0 &&
        strcmp(path + length - 4, "/exe") == 0)
      result = real_readlink("/proc/self/exe", buf, size);
  }
  return result;
}
