#define _GNU_SOURCE
#include <ctype.h>
#include <fcntl.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
  const char prefix[] = "/proc/";
  const char suffix[] = "/exe";
  const char *cursor;

  if (path == NULL || strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
    return 0;
  }
  cursor = path + sizeof(prefix) - 1;
  if (!isdigit((unsigned char)*cursor)) {
    return 0;
  }
  while (isdigit((unsigned char)*cursor)) {
    ++cursor;
  }
  return strcmp(cursor, suffix) == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  const char *resolved = is_proc_pid_exe(path) ? "/proc/self/exe" : path;
  return syscall(SYS_readlinkat, AT_FDCWD, resolved, buffer, size);
}
