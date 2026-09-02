#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
  int consumed = 0;
  if (sscanf(path, "/proc/%*[0-9]/exe%n", &consumed) != 0) {
    return 0;
  }
  return consumed > 0 && path[consumed] == '\0';
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn real_readlink = NULL;
  if (real_readlink == NULL) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (real_readlink == NULL) {
      errno = ENOSYS;
      return -1;
    }
  }
  if (is_proc_pid_exe(path)) {
    return real_readlink("/proc/self/exe", buf, size);
  }
  return real_readlink(path, buf, size);
}
