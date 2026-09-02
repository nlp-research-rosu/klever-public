import Lake
open Lake DSL
package "proof"
require «klean-123-get-odd-collatz» from "./Base"
@[default_target]
lean_lib Proof
