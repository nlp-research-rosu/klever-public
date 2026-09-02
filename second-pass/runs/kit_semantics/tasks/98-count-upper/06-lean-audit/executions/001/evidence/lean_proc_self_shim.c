#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

static int is_proc_pid_exe(const char *path) {
  const char *cursor = path;
  if (strncmp(cursor, "/proc/", 6) != 0) return 0;
  cursor += 6;
  if (*cursor < '0' || *cursor > '9') return 0;
  while (*cursor >= '0' && *cursor <= '9') cursor++;
  return strcmp(cursor, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = real_readlink(path, buf, bufsiz);
  int saved = errno;
  if (result < 0 && saved == ENOENT && is_proc_pid_exe(path)) {
    result = real_readlink("/proc/self/exe", buf, bufsiz);
    saved = errno;
    fprintf(stderr, "SHIM readlink %s -> /proc/self/exe result=%zd errno=%d\n",
            path, result, saved);
  }
  fprintf(stderr, "TRACE readlink path=%s result=%zd errno=%d value=%.*s\n",
          path, result, saved, result > 0 ? (int)result : 0, buf);
  errno = saved;
  return result;
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t bufsiz) {
  static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);
  if (!real_readlinkat) real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  ssize_t result = real_readlinkat(dirfd, path, buf, bufsiz);
  int saved = errno;
  fprintf(stderr, "TRACE readlinkat path=%s result=%zd errno=%d value=%.*s\n",
          path, result, saved, result > 0 ? (int)result : 0, buf);
  errno = saved;
  return result;
}
