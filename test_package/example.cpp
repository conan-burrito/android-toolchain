#include <android/log.h>

int main() {
   __android_log_print(ANDROID_LOG_DEBUG, "[TEST]", "vprint test: %d", 42);
   return 0;
}
