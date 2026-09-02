requires "semantic.k"

module SPEC-VACUITY-AUDITOR
  imports VERIFICATION

  // Deliberately false: for witness X=1,Y=2 the actual result is 2, not 3.
  claim [false-even-upper-off-by-one]:
    <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(Y +Int 1) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <=Int Y andBool Y %Int 2 ==Int 0
endmodule
