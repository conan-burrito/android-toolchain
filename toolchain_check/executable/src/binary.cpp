#include <dce/binary.h>
#include <dcl/library.h>

namespace dce {

std::string binary_call() {
   return dcl::do_call();
}

} // namespace dce