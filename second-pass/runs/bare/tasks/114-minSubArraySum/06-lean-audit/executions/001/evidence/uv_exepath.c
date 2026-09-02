#include <stdio.h>
#include <stddef.h>

extern int uv_exepath(char *buffer, size_t *size);
extern const char *uv_err_name(int error);

int main(void) {
  char buffer[4096];
  size_t size = sizeof(buffer);
  int result = uv_exepath(buffer, &size);
  printf("result=%d name=%s size=%zu path=%s\n",
         result, uv_err_name(result), size, result == 0 ? buffer : "");
  return result == 0 ? 0 : 1;
}
