#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

/*
 * This audit runner exposes a /proc namespace whose numeric PIDs differ from
 * getpid(). Lean 4.22 resolves /proc/<getpid()>/exe, which consequently gets
 * ENOENT. Fall back to the namespace-stable /proc/self/exe only for that one
 * failed procfs lookup.
 */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*next_readlink)(const char *, char *, size_t);
  if (!next_readlink) next_readlink = dlsym(RTLD_NEXT, "readlink");
  ssize_t result = next_readlink(path, buf, size);
  if (result < 0 && errno == ENOENT && strncmp(path, "/proc/", 6) == 0) {
    size_t length = strlen(path);
    if (length > 10 && strcmp(path + length - 4, "/exe") == 0) {
      result = next_readlink("/proc/self/exe", buf, size);
    }
  }
  return result;
}
