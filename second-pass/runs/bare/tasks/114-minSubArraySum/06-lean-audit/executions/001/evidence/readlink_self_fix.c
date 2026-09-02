#define _GNU_SOURCE
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * The audit sandbox exposes /proc/self/exe but not /proc/<numeric-pid>/exe.
 * Lean 4.22's Linux IO.appPath implementation uses the numeric form.
 * Redirect only that exact shape to the equivalent self alias.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
  const char *prefix = "/proc/";
  const char *suffix = "/exe";
  const size_t length = strlen(path);
  const size_t prefix_length = strlen(prefix);
  const size_t suffix_length = strlen(suffix);
  int numeric = length > prefix_length + suffix_length;

  for (size_t index = prefix_length;
       numeric && index < length - suffix_length;
       ++index) {
    numeric = path[index] >= '0' && path[index] <= '9';
  }

  if (numeric &&
      strncmp(path, prefix, prefix_length) == 0 &&
      strcmp(path + length - suffix_length, suffix) == 0) {
    path = "/proc/self/exe";
  }
  return syscall(SYS_readlinkat, AT_FDCWD, path, buffer, size);
}
