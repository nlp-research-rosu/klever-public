#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/* The audit PID namespace reports a PID not mounted in /proc.  Lean only
   needs its own executable path, so map /proc/<self-pid>/exe to procfs's
   namespace-stable /proc/self/exe spelling. */
static const char *portable_proc_path(const char *path) {
  if (strncmp(path, "/proc/", 6) != 0) return path;
  const char *cursor = path + 6;
  if (*cursor < '0' || *cursor > '9') return path;
  while (*cursor >= '0' && *cursor <= '9') cursor++;
  return strcmp(cursor, "/exe") == 0 ? "/proc/self/exe" : path;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  const char *effective = portable_proc_path(path);
  ssize_t result = real_readlink(effective, buf, size);
  int saved = errno;
  fprintf(stderr, "TRACE readlink(%s as %s) -> %zd", path, effective, result);
  if (result >= 0) fprintf(stderr, " value=%.*s", (int)result, buf);
  fputc('\n', stderr);
  errno = saved;
  return result;
}

ssize_t readlinkat(int fd, const char *path, char *buf, size_t size) {
  static ssize_t (*real_readlinkat)(int, const char *, char *, size_t) = NULL;
  if (!real_readlinkat) real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  const char *effective = portable_proc_path(path);
  ssize_t result = real_readlinkat(fd, effective, buf, size);
  int saved = errno;
  fprintf(stderr, "TRACE readlinkat(%d,%s as %s) -> %zd", fd, path, effective, result);
  if (result >= 0) fprintf(stderr, " value=%.*s", (int)result, buf);
  fputc('\n', stderr);
  errno = saved;
  return result;
}
