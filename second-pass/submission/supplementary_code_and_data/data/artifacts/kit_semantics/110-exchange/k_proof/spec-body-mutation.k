requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Both loop conditions are materially mutated from `% 2 == 0` to
  // `% 2 == 1`.  On [2], [2], the original returns "YES" and this mutant
  // returns "NO", so the original postcondition must be rejected.
  claim [odd-count-mutant]:
    <k>
      #loadAll(Module(FuncDef(
        "exchange",
        Params("lst1", "lst2"),
        Expr(Str("Return whether exchanges can make every element of lst1 even."))
        Assign(Name("even_count"), Int(0))
        Assign(Name("value"), Int(0))
        For(
          Name("value"),
          Name("lst1"),
          If(
            Compare(
              BinOp("%", Name("value"), Int(2)),
              CmpOp("==", Int(1))),
            AugAssign(Name("even_count"), "+", Int(1)),
            .Stmts))
        For(
          Name("value"),
          Name("lst2"),
          If(
            Compare(
              BinOp("%", Name("value"), Int(2)),
              CmpOp("==", Int(1))),
            AugAssign(Name("even_count"), "+", Int(1)),
            .Stmts))
        If(
          Compare(
            Name("even_count"),
            CmpOp(">=", Call(Name("len"), Name("lst1"), .Exprs))),
          Return(Str("YES")),
          .Stmts)
        Return(Str("NO")))))
      ~> Call(
           Name("exchange"),
           list(vCons(2, .ValSeq)),
           list(vCons(2, .ValSeq)))
      => str(strToCodes("YES"))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
