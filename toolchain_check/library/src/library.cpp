#include <dcl/config.h>
#include <dcl/library.h>
#include <dcl/version.h>

namespace dcl {

std::string do_call() {
   return std::string(DCL_MESSAGE_TO_RETURN) + ": " + DCL_VERSION_STR;
}

} // namespace dcl
