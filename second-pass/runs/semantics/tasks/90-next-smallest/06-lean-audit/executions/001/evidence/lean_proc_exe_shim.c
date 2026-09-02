#define _GNU_SOURCE
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

extern char *program_invocation_short_name;

static int proc_exe_path(const char *path) {
  size_t length;
  if (path == NULL || strncmp(path, "/proc/", 6) != 0) return 0;
  length = strlen(path);
  return length >= 4 && strcmp(path + length - 4, "/exe") == 0;
}

static const char *pinned_executable(void) {
  const char *name = program_invocation_short_name;
  if (name == NULL) return NULL;
  if (strcmp(name, "lake") == 0)
    return "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake";
  if (strcmp(name, "lean") == 0)
    return "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean";
  return NULL;
}

static ssize_t copy_path(const char *source, char *target, size_t size) {
  size_t length = strlen(source);
  size_t copied = length < size ? length : size;
  memcpy(target, source, copied);
  return (ssize_t)copied;
}

ssize_t readlink(const char *path, char *target, size_t size) {
  static ssize_t (*next_readlink)(const char *, char *, size_t);
  const char *replacement;
  if (next_readlink == NULL)
    next_readlink = dlsym(RTLD_NEXT, "readlink");
  replacement = proc_exe_path(path) ? pinned_executable() : NULL;
  if (replacement != NULL) return copy_path(replacement, target, size);
  return next_readlink(path, target, size);
}

ssize_t readlinkat(
    int directory, const char *path, char *target, size_t size
) {
  static ssize_t (*next_readlinkat)(int, const char *, char *, size_t);
  const char *replacement;
  if (next_readlinkat == NULL)
    next_readlinkat = dlsym(RTLD_NEXT, "readlinkat");
  replacement = proc_exe_path(path) ? pinned_executable() : NULL;
  if (replacement != NULL) return copy_path(replacement, target, size);
  return next_readlinkat(directory, path, target, size);
}
