#define _GNU_SOURCE
#include <ctype.h>
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

static int is_proc_pid_exe(const char *path) {
    static const char prefix[] = "/proc/";
    static const char suffix[] = "/exe";
    if (strncmp(path, prefix, sizeof(prefix) - 1) != 0) return 0;
    const char *cursor = path + sizeof(prefix) - 1;
    if (!isdigit((unsigned char)*cursor)) return 0;
    while (isdigit((unsigned char)*cursor)) cursor++;
    return strcmp(cursor, suffix) == 0;
}

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static readlink_fn real_readlink;
    if (!real_readlink) real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (is_proc_pid_exe(path)) path = "/proc/self/exe";
    return real_readlink(path, buffer, size);
}
