#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_name;

static int is_proc_exe(const char *path) {
  size_t length;
  if (path == NULL || strncmp(path, "/proc/", 6) != 0) return 0;
  length = strlen(path);
  return length >= 4 && strcmp(path + length - 4, "/exe") == 0;
}

static const char *lean_executable(void) {
  const char *name = program_invocation_name;
  if (name == NULL) return NULL;
  if (strstr(name, "/lake") != NULL || strcmp(name, "lake") == 0)
    return "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake";
  if (strstr(name, "/lean") != NULL || strcmp(name, "lean") == 0)
    return "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean";
  return NULL;
}

static ssize_t copy_target(const char *target, char *buffer, size_t size) {
  size_t length = strlen(target);
  size_t copied = length < size ? length : size;
  memcpy(buffer, target, copied);
  return (ssize_t)copied;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
  static ssize_t (*real_readlink)(const char *, char *, size_t);
  const char *target;
  if (real_readlink == NULL)
    real_readlink = dlsym(RTLD_NEXT, "readlink");
  target = is_proc_exe(path) ? lean_executable() : NULL;
  if (target != NULL) return copy_target(target, buffer, size);
  return real_readlink(path, buffer, size);
}

ssize_t readlinkat(int directory, const char *path, char *buffer, size_t size) {
  static ssize_t (*real_readlinkat)(int, const char *, char *, size_t);
  const char *target;
  if (real_readlinkat == NULL)
    real_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  target = is_proc_exe(path) ? lean_executable() : NULL;
  if (target != NULL) return copy_target(target, buffer, size);
  return real_readlinkat(directory, path, buffer, size);
}
