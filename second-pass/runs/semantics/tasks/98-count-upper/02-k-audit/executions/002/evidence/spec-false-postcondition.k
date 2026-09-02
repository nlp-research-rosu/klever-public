requires "verification.k"

module AUDIT-FALSE-POSTCONDITION
  imports COUNT-UPPER-VERIFICATION

  // Fresh A5 mutation: the unchanged real program is falsely required to
  // return one more than countUpperFrom.  The empty string is a satisfying
  // witness: the program and canonical function return 0, while this asks 1.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "count_upper",
            Params("s"),
            Assign(Name("count"), Int(0))
            Assign(Name("even"), Bool(true))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              AugAssign(
                Name("count"),
                "+",
                BoolOp(
                  "and",
                  Name("even"),
                  Compare(Name("ch"), CmpOp("in", Str("AEIOU")))))
              Assign(Name("even"), UnaryOp("not", Name("even")))
              .Stmts)
            Return(Name("count"))
            .Stmts)
          .Stmts))
      ~> Call(Name("count_upper"), str(S:IntSeq))
      => countUpperFrom(S, true) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "count_upper" |->
          closureVal(
            ("s", .ParamNames),
            Assign(Name("count"), Int(0))
            Assign(Name("even"), Bool(true))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              AugAssign(
                Name("count"),
                "+",
                BoolOp(
                  "and",
                  Name("even"),
                  Compare(Name("ch"), CmpOp("in", Str("AEIOU")))))
              Assign(Name("even"), UnaryOp("not", Name("even")))
              .Stmts)
            Return(Name("count"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
