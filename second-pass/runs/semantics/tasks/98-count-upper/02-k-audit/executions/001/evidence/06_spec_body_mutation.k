requires "verification.k"

module COUNT-UPPER-BODY-MUTATION-SPEC
  imports COUNT-UPPER-VERIFICATION

  // Executed program and pinned closure count only 'A'; postcondition still
  // uses countUpperFrom, whose proof-local equations count AEIOU.
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
                  Compare(Name("ch"), CmpOp("in", Str("A")))))
              Assign(Name("even"), UnaryOp("not", Name("even")))
              .Stmts)
            Return(Name("count"))
            .Stmts)
          .Stmts))
      ~> Call(Name("count_upper"), str(S:IntSeq))
      => countUpperFrom(S, true)
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
                  Compare(Name("ch"), CmpOp("in", Str("A")))))
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
