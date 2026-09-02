#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

static void probe_log(const char *format, ...) {
  char buffer[4096];
  va_list arguments;
  va_start(arguments, format);
  int length = vsnprintf(buffer, sizeof(buffer), format, arguments);
  va_end(arguments);
  if (length > 0) {
    size_t count = (size_t)length < sizeof(buffer) ? (size_t)length
                                                   : sizeof(buffer) - 1;
    syscall(SYS_write, STDERR_FILENO, buffer, count);
  }
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  ssize_t result = syscall(SYS_readlink, path, buffer, size);
  int saved_errno = errno;
  if (result < 0 && saved_errno == ENOENT &&
      strncmp(path, "/proc/", 6) == 0 &&
      strlen(path) > 10 &&
      strcmp(path + strlen(path) - 4, "/exe") == 0) {
    result = syscall(SYS_readlink, "/proc/self/exe", buffer, size);
    saved_errno = errno;
    probe_log("PROBE sandbox PID fallback path=%s via=/proc/self/exe "
              "result=%zd errno=%d\n",
              path, result, saved_errno);
  }
  probe_log("PROBE readlink path=%s size=%zu result=%zd errno=%d\n",
            path, size, result, saved_errno);
  errno = saved_errno;
  return result;
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
  ssize_t result = syscall(SYS_readlinkat, directory, path, buffer, size);
  int saved_errno = errno;
  probe_log("PROBE readlinkat dir=%d path=%s size=%zu result=%zd errno=%d\n",
            directory, path, size, result, saved_errno);
  errno = saved_errno;
  return result;
}

char *realpath(const char *path, char *resolved) {
  static char *(*real_realpath)(const char *, char *);
  if (real_realpath == NULL) {
    real_realpath = dlsym(RTLD_NEXT, "realpath");
  }
  char *result = real_realpath(path, resolved);
  int saved_errno = errno;
  probe_log("PROBE realpath path=%s result=%s errno=%d\n",
            path, result == NULL ? "(null)" : result, saved_errno);
  errno = saved_errno;
  return result;
}

char *getcwd(char *buffer, size_t size) {
  static char *(*real_getcwd)(char *, size_t);
  if (real_getcwd == NULL) {
    real_getcwd = dlsym(RTLD_NEXT, "getcwd");
  }
  char *result = real_getcwd(buffer, size);
  int saved_errno = errno;
  probe_log("PROBE getcwd size=%zu result=%s errno=%d\n",
            size, result == NULL ? "(null)" : result, saved_errno);
  errno = saved_errno;
  return result;
}
