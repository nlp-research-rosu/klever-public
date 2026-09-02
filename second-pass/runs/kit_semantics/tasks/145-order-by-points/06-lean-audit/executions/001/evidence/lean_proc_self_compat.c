#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_numeric_proc_exe(const char *path) {
  const char *p;
  if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
    return 0;
  }
  p = path + 6;
  if (!isdigit((unsigned char)*p)) {
    return 0;
  }
  while (isdigit((unsigned char)*p)) {
    p++;
  }
  return strcmp(p, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t size) {
  static readlink_fn real_readlink = NULL;
  if (real_readlink == NULL) {
    real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
  }
  if (is_numeric_proc_exe(path)) {
    return real_readlink("/proc/self/exe", buf, size);
  }
  return real_readlink(path, buf, size);
}
