requires "semantic.k"

module SPEC-VACUITY-FRESH
  imports VERIFICATION

  // Deliberately false: for X=1,Y=2 the real program returns 2, not 4.
  claim <k> Run(chooseNumProgram, Int(X), Int(Y))
             => VInt(Y +Int 2) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <=Int Y andBool Y %Int 2 ==Int 0
endmodule
