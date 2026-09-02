#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/*
 * Lean 4.22 resolves its executable via /proc/<getpid()>/exe.  The audit
 * sandbox's PID namespace and mounted /proc disagree, while /proc/self/exe is
 * correct.  Retry only a missing /proc/<pid>/exe path through /proc/self/exe.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next_fn)(const char *, char *, size_t) = NULL;
  if (!next_fn) next_fn = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = next_fn(path, buf, size);
  int saved = errno;
  size_t length = strlen(path);
  if (result < 0 && saved == ENOENT && strncmp(path, "/proc/", 6) == 0 &&
      length >= 10 && strcmp(path + length - 4, "/exe") == 0 &&
      strcmp(path, "/proc/self/exe") != 0) {
    result = next_fn("/proc/self/exe", buf, size);
    saved = errno;
    fprintf(stderr,
            "PROC_EXE_COMPAT retried %s as /proc/self/exe result=%zd errno=%d\n",
            path, result, saved);
  }
  errno = saved;
  return result;
}
