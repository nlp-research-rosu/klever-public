requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false: derivative([1, 2, 3]) is [2, 6], not [2, 7].
  claim [false-postcondition]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "derivative",
            Params("xs"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("i"), Int(0))
            Assign(Name("x"), NoneVal)
            For(
              Name("x"),
              Name("xs"),
              If(
                Compare(Name("i"), CmpOp(">", Int(0))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    (BinOp("*", Name("i"), Name("x")), .Exprs))),
                .Stmts)
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              .Stmts)
            Return(Name("result"))
            .Stmts)))
      ~> Call(
           Name("derivative"),
           (list(vCons(1, vCons(2, vCons(3, .ValSeq)))), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(2, vCons(7, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
