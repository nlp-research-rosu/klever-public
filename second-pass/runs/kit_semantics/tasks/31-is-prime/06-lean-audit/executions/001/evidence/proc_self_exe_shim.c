#define _GNU_SOURCE
#include <ctype.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

/* The audit sandbox exposes /proc/self/exe but hides /proc/<pid>/exe. */
static int is_numeric_proc_exe(const char *path) {
  const char *cursor;
  if (strncmp(path, "/proc/", 6) != 0) return 0;
  cursor = path + 6;
  if (!isdigit((unsigned char)*cursor)) return 0;
  while (isdigit((unsigned char)*cursor)) cursor++;
  return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  if (is_numeric_proc_exe(path)) path = "/proc/self/exe";
  return syscall(SYS_readlink, path, buf, size);
}
