#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int uv_exepath(char *buffer, size_t *size);

int main(void) {
    char buffer[8192];
    size_t size = sizeof(buffer);
    int result = uv_exepath(buffer, &size);
    if (result == 0 && size < sizeof(buffer)) {
        buffer[size] = '\0';
    } else {
        buffer[0] = '\0';
    }
    printf("result=%d size=%zu path=%s\n", result, size, buffer);
    char proc_path[128];
    char destination[8192];
    memset(destination, 0, sizeof(destination));
    snprintf(proc_path, sizeof(proc_path), "/proc/%d/exe", getpid());
    ssize_t numeric_result =
        readlink(proc_path, destination, sizeof(destination));
    printf(
        "pid=%d proc_path=%s readlink_result=%zd path=%s\n",
        getpid(),
        proc_path,
        numeric_result,
        destination
    );
    return result == 0 && numeric_result >= 0 ? 0 : 1;
}
