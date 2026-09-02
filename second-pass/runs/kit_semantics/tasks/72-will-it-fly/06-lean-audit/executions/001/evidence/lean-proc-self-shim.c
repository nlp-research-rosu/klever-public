#define _GNU_SOURCE
#include <ctype.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

static int is_pid_exe_path(const char *path) {
  static const char prefix[] = "/proc/";
  const char *cursor;
  if (strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
    return 0;
  }
  cursor = path + sizeof(prefix) - 1;
  if (!isdigit((unsigned char)*cursor)) {
    return 0;
  }
  while (isdigit((unsigned char)*cursor)) {
    cursor++;
  }
  return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  const char *resolved = is_pid_exe_path(path) ? "/proc/self/exe" : path;
  return syscall(SYS_readlink, resolved, buffer, size);
}
