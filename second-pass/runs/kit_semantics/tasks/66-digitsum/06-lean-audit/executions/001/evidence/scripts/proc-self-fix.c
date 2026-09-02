#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <limits.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

typedef char *(*realpath_fn)(const char *, char *);
typedef char *(*realpath_chk_fn)(const char *, char *, size_t);

pid_t getpid(void) {
    char buffer[4096];
    ssize_t count;
    int fd = open("/proc/self/status", O_RDONLY);
    if (fd >= 0) {
        count = read(fd, buffer, sizeof(buffer) - 1);
        close(fd);
        if (count > 0) {
            char *line;
            buffer[count] = '\0';
            line = strstr(buffer, "Pid:\t");
            if (line != NULL) {
                long value = strtol(line + 5, NULL, 10);
                if (value > 0) {
                    return (pid_t)value;
                }
            }
        }
    }
    return (pid_t)1;
}

static const char *proc_self_path(const char *path) {
    size_t length;
    if (path == NULL || strncmp(path, "/proc/", 6) != 0) {
        return path;
    }
    length = strlen(path);
    if (length > 10 && strcmp(path + length - 4, "/exe") == 0 &&
        strcmp(path, "/proc/self/exe") != 0) {
        return "/proc/self/exe";
    }
    return path;
}

char *realpath(const char *path, char *resolved_path) {
    static realpath_fn original;
    if (original == NULL) {
        original = (realpath_fn)dlsym(RTLD_NEXT, "realpath");
    }
    return original(proc_self_path(path), resolved_path);
}

char *__realpath_chk(const char *path, char *resolved_path, size_t length) {
    static realpath_chk_fn original;
    if (original == NULL) {
        original = (realpath_chk_fn)dlsym(RTLD_NEXT, "__realpath_chk");
    }
    return original(proc_self_path(path), resolved_path, length);
}
