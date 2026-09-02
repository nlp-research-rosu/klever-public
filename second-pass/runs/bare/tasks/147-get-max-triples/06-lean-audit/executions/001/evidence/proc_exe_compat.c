#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

/*
 * Compatibility for the audit sandbox's mismatched PID/proc namespaces.
 * Retry only a failed /proc/<numeric-pid>/exe lookup as /proc/self/exe.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) {
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  }
  ssize_t result = real_readlink(path, buf, size);
  if (result >= 0 || errno != ENOENT) {
    return result;
  }
  if (strncmp(path, "/proc/", 6) != 0) {
    return result;
  }
  const char *cursor = path + 6;
  if (*cursor < '0' || *cursor > '9') {
    return result;
  }
  while (*cursor >= '0' && *cursor <= '9') {
    ++cursor;
  }
  if (strcmp(cursor, "/exe") != 0) {
    return result;
  }
  return real_readlink("/proc/self/exe", buf, size);
}
