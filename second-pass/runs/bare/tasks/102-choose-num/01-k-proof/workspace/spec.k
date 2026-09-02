requires "semantic.k"

module SPEC
  imports VERIFICATION

  // Empty interval: there is no integer, and hence no even integer, in [X,Y].
  claim <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(-1) </k>
    requires 0 <Int X andBool 0 <Int Y andBool X >Int Y

  // Nonempty interval with an even upper endpoint: Y itself is the maximum.
  claim <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(Y) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <=Int Y andBool Y %Int 2 ==Int 0

  // An odd upper endpoint with room below it: Y-1 is in range and is the
  // greatest even integer because it is immediately below Y.
  claim <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(Y -Int 1) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <Int Y andBool Y %Int 2 =/=Int 0

  // The only nonempty interval without an even candidate is [odd, odd].
  claim <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(-1) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X ==Int Y andBool Y %Int 2 =/=Int 0

  // End-to-end contract over the same exhaustive partition: execution
  // produces either the required sentinel, or an in-range even result whose
  // next possible even successor exceeds Y.
  claim <k> Run(chooseNumProgram, Int(X), Int(Y))
             ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y andBool X >Int Y

  claim <k> Run(chooseNumProgram, Int(X), Int(Y))
             ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <=Int Y andBool Y %Int 2 ==Int 0

  claim <k> Run(chooseNumProgram, Int(X), Int(Y))
             ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <Int Y andBool Y %Int 2 =/=Int 0

  claim <k> Run(chooseNumProgram, Int(X), Int(Y))
             ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X ==Int Y andBool Y %Int 2 =/=Int 0
endmodule
