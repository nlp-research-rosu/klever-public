#define _GNU_SOURCE

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <sys/auxv.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

ssize_t readlink(const char *restrict path, char *restrict buffer, size_t size) {
  long requested_pid = -1;
  char trailing = '\0';
  if (sscanf(path, "/proc/%ld/exe%c", &requested_pid, &trailing) == 1 &&
      requested_pid == (long)getpid()) {
    const char *execfn = (const char *)getauxval(AT_EXECFN);
    if (execfn == NULL) {
      errno = ENOENT;
      return -1;
    }
    size_t length = strlen(execfn);
    size_t copied = length < size ? length : size;
    memcpy(buffer, execfn, copied);
    return (ssize_t)copied;
  }
  return syscall(SYS_readlink, path, buffer, size);
}
