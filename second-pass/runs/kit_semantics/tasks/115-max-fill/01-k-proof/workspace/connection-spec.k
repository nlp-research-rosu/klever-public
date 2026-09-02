requires "verification.k"

// This module is proved against a definition whose main module is
// MAX-FILL-SUMMARY, so neither dispatch twin in MAX-FILL-VERIFICATION exists
// in the executable theory.
module MAX-FILL-CONNECTION-SPEC
  imports MAX-FILL-SUMMARY

  claim [fixed-int-of]:
    <k> intOf(I:Int) => I ... </k>

  claim [fixed-sum-dispatch]:
    <k> #applyK(toCall(builtinV("sum")), (list(VS:ValSeq), .Vals))
          => #sumAcc(list(VS), 0) ... </k>
endmodule
