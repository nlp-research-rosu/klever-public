requires "verification.k"

module ADD-SPEC
  imports ADD-VERIFICATION

  // ---- Entry claim — result = add(X, Y) == X +Int Y, for symbolic ints X, Y.
  claim
    <k>
      FuncDef("add", Params("x", "y"), Return(BinOp("+", Name("x"), Name("y"))))
      Assign(Name("result"), Call(Name("add"), X:Int, Y:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "add" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Int X +Int Y
    [all-path]
endmodule
