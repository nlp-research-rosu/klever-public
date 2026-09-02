requires "reference-semantics/semantics.k"

module ANY-INT-VERIFICATION-BODY-MUT
  imports MPY

  // Material mutation of the executed program term: always return false.
  syntax Stmts ::= "anyIntBodyMut" [function, total]
  rule anyIntBodyMut => Return(Bool(false)) .Stmts

  syntax KItem ::= "#anyIntMut" "(" Val "," Val "," Val ")"
  rule <k> #anyIntMut(X:Val, Y:Val, Z:Val)
        => #applyK(
             toCall(closureVal(("x", "y", "z"), anyIntBodyMut, 0)),
             (X, Y, Z, .Vals))
         ... </k>

  syntax Bool ::= sumConditionMut(Int, Int, Int) [function, total]
  rule sumConditionMut(X:Int, Y:Int, Z:Int)
    => ((X +Int Y) ==Int Z)
       orBool ((X +Int Z) ==Int Y)
       orBool ((Y +Int Z) ==Int X)
endmodule
