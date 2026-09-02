requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [can-arrange-loop]:
    <k>
      (#loop(
        list(VS),
        Name("value"),
        If(
          Compare(Name("i"), CmpOp(">", Int(0))),
          If(
            UnaryOp(
              "not",
              Compare(
                Name("value"),
                CmpOp(">=", Name("previous")))),
            Assign(Name("index"), Name("i")),
            .Stmts),
          .Stmts)
        Assign(Name("previous"), Name("value"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
        .Stmts)
      => .K)
      ~> (Return(Name("index")) .Stmts)
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "can_arrange" |->
          closureVal(
            "arr", .ParamNames,
            Assign(Name("index"), UnaryOp("-", Int(1)))
            Assign(Name("i"), Int(0))
            Assign(Name("previous"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"), Name("arr"),
              If(
                Compare(Name("i"), CmpOp(">", Int(0))),
                If(
                  UnaryOp(
                    "not",
                    Compare(
                      Name("value"),
                      CmpOp(">=", Name("previous")))),
                  Assign(Name("index"), Name("i")),
                  .Stmts),
                .Stmts)
              Assign(Name("previous"), Name("value"))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              .Stmts)
            Return(Name("index"))
            .Stmts,
            0),
        parent(-1))
      1  |-> scope(
        "arr"      |-> list(ORIG)
        "i"        |-> (I => ?FINAL_I:Int)
        "index"    |-> (A => arrangeSeq(VS, I, P, A))
        "previous" |-> (P => ?FINAL_PREVIOUS:Val)
        "value"    |-> (P => ?FINAL_VALUE:Val),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0
     andBool scanDefined(VS, I, P)

  claim [can-arrange]:
    <k>
      (#loadAll(
        Module(
          FuncDef(
            "can_arrange", Params("arr"),
            Assign(Name("index"), UnaryOp("-", Int(1)))
            Assign(Name("i"), Int(0))
            Assign(Name("previous"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"), Name("arr"),
              If(
                Compare(Name("i"), CmpOp(">", Int(0))),
                If(
                  UnaryOp(
                    "not",
                    Compare(
                      Name("value"),
                      CmpOp(">=", Name("previous")))),
                  Assign(Name("index"), Name("i")),
                  .Stmts),
                .Stmts)
              Assign(Name("previous"), Name("value"))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              .Stmts)
            Return(Name("index"))
            .Stmts)
          .Stmts))
      ~> Call(Name("can_arrange"), list(VS))
      => arrangeSeq(VS, 0, 0, -1))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        .Map
        => "can_arrange" |->
             closureVal(
               "arr", .ParamNames,
               Assign(Name("index"), UnaryOp("-", Int(1)))
               Assign(Name("i"), Int(0))
               Assign(Name("previous"), Int(0))
               Assign(Name("value"), Int(0))
               For(
                 Name("value"), Name("arr"),
                 If(
                   Compare(Name("i"), CmpOp(">", Int(0))),
                   If(
                     UnaryOp(
                       "not",
                       Compare(
                         Name("value"),
                         CmpOp(">=", Name("previous")))),
                     Assign(Name("index"), Name("i")),
                     .Stmts),
                   .Stmts)
                 Assign(Name("previous"), Name("value"))
                 Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
                 .Stmts)
               Return(Name("index"))
               .Stmts,
               0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires scanDefined(VS, 0, 0)
endmodule
