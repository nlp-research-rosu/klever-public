requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // The body mutation changes the real entry base case from False to True.
  // The original result obligation must therefore fail on this satisfying input.
  claim [body-sensitivity]:
    <k> verifyMutant(VList(.PValues), VInt(0)) => VBool(false) </k>
endmodule
