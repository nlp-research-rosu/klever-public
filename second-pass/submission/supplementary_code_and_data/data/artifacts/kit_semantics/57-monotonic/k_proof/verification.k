requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  rule A:Bool ==Bool (A orBool B:Bool) => true
    requires A
    [simplification]

  rule B:Bool ==Bool (A:Bool orBool B) => true
    requires notBool A
    [simplification]
endmodule
