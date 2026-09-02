#define _GNU_SOURCE
#include <ctype.h>
#include <stddef.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * This audit container exposes /proc/self/exe but not /proc/<getpid()>/exe.
 * Lean 4.22 uses the latter to locate itself. Redirect only the current
 * process's exact executable lookup to the equivalent /proc/self spelling.
 */
static const char *fix_self_exe(const char *path) {
  const char prefix[] = "/proc/";
  const char suffix[] = "/exe";
  if (strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
    return path;
  }
  const char *cursor = path + sizeof(prefix) - 1;
  if (!isdigit((unsigned char)*cursor)) {
    return path;
  }
  pid_t observed_pid = 0;
  while (isdigit((unsigned char)*cursor)) {
    observed_pid = observed_pid * 10 + (*cursor - '0');
    cursor++;
  }
  return observed_pid == getpid() && strcmp(cursor, suffix) == 0
      ? "/proc/self/exe"
      : path;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  return syscall(SYS_readlink, fix_self_exe(path), buffer, size);
}

ssize_t readlinkat(
    int directory, const char *path, char *buffer, size_t size
) {
  return syscall(
      SYS_readlinkat, directory, fix_self_exe(path), buffer, size
  );
}
