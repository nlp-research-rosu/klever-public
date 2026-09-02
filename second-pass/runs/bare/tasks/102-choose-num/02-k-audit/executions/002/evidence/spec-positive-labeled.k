requires "semantic.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [exact-empty]:
    <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(-1) </k>
    requires 0 <Int X andBool 0 <Int Y andBool X >Int Y

  claim [exact-even-upper]:
    <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(Y) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <=Int Y andBool Y %Int 2 ==Int 0

  claim [exact-odd-upper-with-room]:
    <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(Y -Int 1) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <Int Y andBool Y %Int 2 =/=Int 0

  claim [exact-odd-singleton]:
    <k> Run(chooseNumProgram, Int(X), Int(Y)) => VInt(-1) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X ==Int Y andBool Y %Int 2 =/=Int 0

  claim [contract-empty]:
    <k> Run(chooseNumProgram, Int(X), Int(Y))
         ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y andBool X >Int Y

  claim [contract-even-upper]:
    <k> Run(chooseNumProgram, Int(X), Int(Y))
         ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <=Int Y andBool Y %Int 2 ==Int 0

  claim [contract-odd-upper-with-room]:
    <k> Run(chooseNumProgram, Int(X), Int(Y))
         ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X <Int Y andBool Y %Int 2 =/=Int 0

  claim [contract-odd-singleton]:
    <k> Run(chooseNumProgram, Int(X), Int(Y))
         ~> checkChooseNum(X, Y) => VBool(true) </k>
    requires 0 <Int X andBool 0 <Int Y
     andBool X ==Int Y andBool Y %Int 2 =/=Int 0
endmodule
