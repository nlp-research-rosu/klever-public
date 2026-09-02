requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false: for the realizable two-element witness constrained
  // by pairNear(A,B,T), the loop must finish with found == true, not false.
  claim [false-result]:
    <k>
      #loop(
        list(vCons(A:Float, vCons(B:Float, .ValSeq))),
        Name("number1"),
        Assign(Name("j"), Int(0))
        For(Name("number2"), Name("numbers"),
          If(Compare(Name("i"), CmpOp("<", Name("j"))),
            If(
              Compare(
                Call(Name("abs"),
                  BinOp("-", Name("number1"), Name("number2"))),
                CmpOp("<", Name("threshold"))),
              Assign(Name("found"), Bool(true)),
              .Stmts),
            .Stmts)
          Assign(Name("j"), BinOp("+", Name("j"), Int(1))))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      0  |-> scope("has_close_elements" |-> _CLOSURE:Val, parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
        "numbers"  |-> list(vCons(A, vCons(B, .ValSeq)))
        "threshold"|-> T:Float
        "found"    |-> (false => false)
        "i"        |-> (0 => 2)
        "j"        |-> (0 => ?JFinal:Int)
        "number1"  |-> (0.0 => ?N1Final:Val)
        "number2"  |-> (0.0 => ?N2Final:Val),
        parent(0))
    </scopes>
    <heap> .Map </heap>
    requires pairNear(A, B, T)
endmodule
