requires "verification.k"

module AUDIT-SPEC-ENTRY
  imports INTERSPERSE-VERIFICATION

  claim
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List")
        FuncDef("intersperse", Params("numbers", "delimeter"),
          Assign(Name("result"), ListExpr(.Exprs))
          For(Name("number"), Name("numbers"),
            If(Name("result"),
              Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
              .Stmts)
            Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
          Return(Name("result")))))
      ~> Call(Name("intersperse"), list(NUMBERS), D)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "intersperse" |-> closureVal(
          ("numbers", "delimeter"),
          Assign(Name("result"), ListExpr(.Exprs))
          For(Name("number"), Name("numbers"),
            If(Name("result"),
              Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
              .Stmts)
            Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
          Return(Name("result")),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(intersperseVS(NUMBERS, D)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
