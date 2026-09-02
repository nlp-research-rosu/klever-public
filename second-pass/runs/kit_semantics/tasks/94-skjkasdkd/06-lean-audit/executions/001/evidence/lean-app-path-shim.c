#define _GNU_SOURCE
#include <errno.h>
#include <ctype.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * The audit sandbox makes Lean's libuv uv_exepath/readlink("/proc/self/exe")
 * fail, although the pinned binaries themselves are readable and executable.
 * Supply only that process-image lookup from the pinned toolchain path.  Every
 * other readlink remains the raw kernel operation.
 */
extern char *program_invocation_short_name;

static int is_process_exe_path(const char *path) {
  if (strcmp(path, "/proc/self/exe") == 0) {
    return 1;
  }
  static const char prefix[] = "/proc/";
  if (strncmp(path, prefix, sizeof(prefix) - 1) != 0) {
    return 0;
  }
  const char *cursor = path + sizeof(prefix) - 1;
  if (!isdigit((unsigned char)*cursor)) {
    return 0;
  }
  while (isdigit((unsigned char)*cursor)) {
    ++cursor;
  }
  return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  if (is_process_exe_path(path)) {
    static const char prefix[] =
        "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/";
    char resolved[PATH_MAX];
    int written = snprintf(
        resolved, sizeof(resolved), "%s%s",
        prefix, program_invocation_short_name
    );
    if (written < 0 || (size_t)written >= sizeof(resolved)) {
      errno = ENAMETOOLONG;
      return -1;
    }
    size_t length = (size_t)written;
    if (length > size) {
      length = size;
    }
    memcpy(buffer, resolved, length);
    return (ssize_t)length;
  }
  return syscall(SYS_readlink, path, buffer, size);
}

ssize_t readlinkat(int dirfd, const char *path, char *buffer, size_t size) {
  if (is_process_exe_path(path)) {
    return readlink(path, buffer, size);
  }
  return syscall(SYS_readlinkat, dirfd, path, buffer, size);
}
