#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <string.h>
#include <unistd.h>

static int is_namespaced_proc_exe(const char *path) {
  const char prefix[] = "/proc/";
  if (strncmp(path, prefix, sizeof(prefix) - 1) != 0) return 0;
  path += sizeof(prefix) - 1;
  if (!isdigit((unsigned char)*path)) return 0;
  while (isdigit((unsigned char)*path)) path++;
  return strcmp(path, "/exe") == 0;
}

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
  static ssize_t (*next_readlink)(const char *, char *, size_t) = NULL;
  if (!next_readlink) next_readlink = dlsym(RTLD_NEXT, "readlink");
  if (is_namespaced_proc_exe(path)) path = "/proc/self/exe";
  return next_readlink(path, buf, bufsiz);
}

ssize_t readlinkat(int dirfd, const char *path, char *buf, size_t bufsiz) {
  static ssize_t (*next_readlinkat)(int, const char *, char *, size_t) = NULL;
  if (!next_readlinkat) next_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  if (is_namespaced_proc_exe(path)) path = "/proc/self/exe";
  return next_readlinkat(dirfd, path, buf, bufsiz);
}
