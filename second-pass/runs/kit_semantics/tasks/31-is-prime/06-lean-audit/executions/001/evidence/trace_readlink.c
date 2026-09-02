#define _GNU_SOURCE
#include <errno.h>
#include <stdio.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t size) {
  ssize_t result = syscall(SYS_readlink, path, buf, size);
  int saved = errno;
  fprintf(stderr, "TRACE readlink path=%s result=%zd errno=%d pid=%ld\n",
          path, result, saved, (long)syscall(SYS_getpid));
  errno = saved;
  return result;
}
