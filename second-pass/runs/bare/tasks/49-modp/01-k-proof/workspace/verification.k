requires "semantic.k"

module MODP-VERIFICATION
  imports MODP-SEMANTIC

  // The mathematical contract, using K's unbounded-integer modular power.
  syntax Int ::= expectedModp(Int, Int) [function]
  rule expectedModp(N, P) => 2 ^%Int N P
endmodule
