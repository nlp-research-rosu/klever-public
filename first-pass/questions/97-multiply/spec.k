requires "verification.k"

module MULTIPLY-SPEC
  imports MULTIPLY-VERIFICATION

  claim
    <k>
      FuncDef("multiply", Params("a", "b"),
        Return(BinOp("*",
          Call(Name("abs"), BinOp("%", Name("a"), Int(10))),
          Call(Name("abs"), BinOp("%", Name("b"), Int(10))))))
      Assign(Name("result"), Call(Name("multiply"), A:Int , B:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "multiply" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Int absInt(pyMod(A, 10)) *Int absInt(pyMod(B, 10))
    [all-path]
endmodule
