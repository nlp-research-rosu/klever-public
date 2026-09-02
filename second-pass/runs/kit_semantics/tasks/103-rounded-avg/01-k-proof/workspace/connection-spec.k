requires "verification-base.k"

module LOOP-CONNECTION
  imports VERIFICATION-BASE

  claim [binary-loop-exact]:
    <k>
      #while(
        Compare(Name("value"), CmpOp(">", Int(1))),
        Assign(
          Name("digits"),
          BinOp(
            "+",
            Call(
              Name("chr"),
              BinOp("+", Int(48), BinOp("%", Name("value"), Int(2)))),
            Name("digits")))
        Assign(Name("value"), BinOp("//", Name("value"), Int(2))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(MODULE:Map, parent(-1))
      1 |-> scope(
        "n" |-> NI:Int
        "m" |-> MI:Int
        "value" |-> (V:Int => 1)
        "digits" |-> (str(A:IntSeq) => str(loopDigits(V, A))),
        parent(0))
    </scopes>
    requires V >Int 0
      andBool allBits(A)
      andBool notBool ("chr" in_keys(MODULE))
    ensures bitWeight(loopDigits(V, A))
              +Int bitValue(loopDigits(V, A))
            ==Int V *Int bitWeight(A) +Int bitValue(A)
      andBool allBits(loopDigits(V, A))
endmodule
