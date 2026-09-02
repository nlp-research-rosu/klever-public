import Lake
open Lake DSL
package "proof"
require «klean-40-triples-sum-to-zero» from "./Base"
@[default_target]
lean_lib Proof
