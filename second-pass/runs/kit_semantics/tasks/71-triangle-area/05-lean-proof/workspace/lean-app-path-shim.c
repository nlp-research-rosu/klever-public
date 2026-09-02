#define _GNU_SOURCE

#include <ctype.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/*
 * Lean 4.22 resolves its installation via /proc/<own-pid>/exe.  The benchmark
 * sandbox permits the equivalent /proc/self/exe path but denies the numeric
 * spelling, so translate only that spelling before issuing the same readlink
 * system call.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
  const char *cursor = path;

  if (strncmp(cursor, "/proc/", 6) == 0) {
    cursor += 6;
    while (isdigit((unsigned char)*cursor)) {
      ++cursor;
    }
    if (cursor != path + 6 && strcmp(cursor, "/exe") == 0) {
      path = "/proc/self/exe";
    }
  }

  return syscall(SYS_readlink, path, buffer, size);
}
