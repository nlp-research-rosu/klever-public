requires "verification.k"

module RIGHT-ANGLE-TRIANGLE-SPEC
  imports RIGHT-ANGLE-TRIANGLE-VERIFICATION

  claim
    <k>
      FuncDef("right_angle_triangle", Params("a", "b", "c"),
        Return(BoolOp("or",
          Compare(BinOp("*", Name("a"), Name("a")), CmpOp("==", BinOp("+", BinOp("*", Name("b"), Name("b")), BinOp("*", Name("c"), Name("c"))))),
          Compare(BinOp("*", Name("b"), Name("b")), CmpOp("==", BinOp("+", BinOp("*", Name("a"), Name("a")), BinOp("*", Name("c"), Name("c"))))),
          Compare(BinOp("*", Name("c"), Name("c")), CmpOp("==", BinOp("+", BinOp("*", Name("a"), Name("a")), BinOp("*", Name("b"), Name("b"))))))))
      Assign(Name("result"), Call(Name("right_angle_triangle"), A:Int , B:Int , C:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "right_angle_triangle" <- ?_:Val ] [ "result" <- ?R:Bool ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool (A *Int A ==Int B *Int B +Int C *Int C)
             orBool (B *Int B ==Int A *Int A +Int C *Int C)
             orBool (C *Int C ==Int A *Int A +Int B *Int B)
    [all-path]
endmodule
