#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

/*
 * The audit sandbox places processes in a PID namespace while exposing a
 * differently scoped /proc. Lean asks readlink("/proc/<getpid()>/exe"), which
 * therefore returns ENOENT. /proc/self/exe is namespace-independent here.
 */
static int is_proc_pid_exe(const char *path) {
  if (strncmp(path, "/proc/", 6) != 0) return 0;
  const char *cursor = path + 6;
  if (!isdigit((unsigned char)*cursor)) return 0;
  while (isdigit((unsigned char)*cursor)) cursor++;
  return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next)(const char *, char *, size_t);
  if (!next) next = dlsym(RTLD_NEXT, "readlink");
  if (is_proc_pid_exe(path)) path = "/proc/self/exe";
  return next(path, buf, size);
}
