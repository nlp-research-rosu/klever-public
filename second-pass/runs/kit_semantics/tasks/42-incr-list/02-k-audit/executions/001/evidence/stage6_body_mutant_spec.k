requires "verification.k"

module AUDIT-BODY-MUTANT-SPEC
  imports VERIFICATION

  // The executed program term is materially changed from x + 1 to x + 2.
  // On ground input [0], the unchanged intended postcondition [1] must fail.
  claim [audit-body-mutant]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "incr_list",
            Params("l"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("x"), Int(0))
            For(
              Name("x"),
              Name("l"),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  (BinOp("+", Name("x"), Int(2)), .Exprs)))
              .Stmts)
            Return(Name("result"))
            .Stmts)
          .Stmts))
      ~> Call(Name("incr_list"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "incr_list" |->
           closureVal(
             "l",
             Assign(Name("result"), ListExpr(.Exprs))
             Assign(Name("x"), Int(0))
             For(
               Name("x"),
               Name("l"),
               Expr(
                 Call(
                   Attribute(Name("result"), "append"),
                   (BinOp("+", Name("x"), Int(2)), .Exprs)))
               .Stmts)
             Return(Name("result"))
             .Stmts,
             0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(vCons(0, .ValSeq))
      =>
      0 |-> list(vCons(0, .ValSeq))
      1 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
