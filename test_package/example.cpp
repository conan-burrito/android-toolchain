// Test C++ support, include directories and android headers
#include <android/log.h>

#include <cstddef>
#include <string>
#include <iostream>

int main() {
   std::string str("Hello world");
   std::cout << str << std::endl;
   __android_log_print(ANDROID_LOG_DEBUG, "[TEST]", "vprint test: %d", 42);
   return 0;
}
