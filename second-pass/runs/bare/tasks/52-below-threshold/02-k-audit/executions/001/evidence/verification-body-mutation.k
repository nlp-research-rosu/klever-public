requires "semantic.k"

module VERIFICATION-BODY-MUTATION
  imports MPY

  syntax Bool ::= allBelowBodyMutation(IntSeq, Int) [function, total]
  rule allBelowBodyMutation(nil, _T) => true
  rule allBelowBodyMutation(cons(I, XS), T)
    => (I <Int T) andBool allBelowBodyMutation(XS, T)

  syntax Pgm ::= "bodyMutatedProgram" [macro]
  rule bodyMutatedProgram
    => Module(
         FuncDef("below_threshold", Params("l", "t"),
           Return(Bool(true))))
endmodule
