requires "verification.k"

module COMPARE-ONE-SPEC
  imports COMPARE-ONE-VERIFICATION

  // ---- A = int, B = int (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), I1:Int, I2:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(I1, I2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = int, B = float (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), I1:Int, F2:Float))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(I1, F2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = int, B = str (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), I1:Int, str(CS2:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(I1, str(CS2)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = float, B = int (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), F1:Float, I2:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(F1, I2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = float, B = float (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), F1:Float, F2:Float))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(F1, F2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = float, B = str (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), F1:Float, str(CS2:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(F1, str(CS2)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = str, B = int (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), str(CS1:IntSeq), I2:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(str(CS1), I2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = str, B = float (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), str(CS1:IntSeq), F2:Float))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(str(CS1), F2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- A = str, B = str (sort-pinned: [owise] isinstance rules need the
  // constructor known; the backend does not narrow raw Vals here)
  claim
    <k>
      FuncDef("compare_one", Params("a", "b"),
        Assign(
          TupleExpr(Name("temp_a"), Name("temp_b")),
          TupleExpr(Name("a"), Name("b")))
        If(Call(Name("isinstance"), Name("temp_a"), Name("str")),
          Assign(
            Name("temp_a"),
            Call(Attribute(Name("temp_a"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Call(Name("isinstance"), Name("temp_b"), Name("str")),
          Assign(
            Name("temp_b"),
            Call(Attribute(Name("temp_b"), "replace"), Str(","), Str("."))),
          .Stmts)
        If(Compare(
          Call(Name("float"), Name("temp_a")),
          CmpOp("==", Call(Name("float"), Name("temp_b")))),
          Return(NoneVal),
          .Stmts)
        Return(
          IfExp(
            Compare(
              Call(Name("float"), Name("temp_a")),
              CmpOp(">", Call(Name("float"), Name("temp_b")))),
            Name("a"),
            Name("b"))))
      Assign(Name("result"), Call(Name("compare_one"), str(CS1:IntSeq), str(CS2:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "compare_one" <- ?_:Val ]
                       [ "result" <- compareRes(str(CS1), str(CS2)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
