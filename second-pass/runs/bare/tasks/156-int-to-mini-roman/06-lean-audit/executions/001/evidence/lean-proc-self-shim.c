#define _GNU_SOURCE
#include <dlfcn.h>
#include <ctype.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
  if (strncmp(path, "/proc/", 6) != 0) return 0;
  const char *cursor = path + 6;
  if (!isdigit((unsigned char)*cursor)) return 0;
  while (isdigit((unsigned char)*cursor)) cursor++;
  return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn next = NULL;
  if (next == NULL) next = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  return next(is_proc_pid_exe(path) ? "/proc/self/exe" : path, buf, size);
}
