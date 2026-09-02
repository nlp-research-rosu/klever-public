requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Satisfiable witness: the original program on ["a"] returns "a", not "".
  claim [false-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "find_max",
            Params("words"),
            Assign(Name("result"), Str(""))
            Assign(Name("max_unique"), UnaryOp("-", Int(1)))
            Assign(Name("word"), Str(""))
            Assign(Name("unique"), UnaryOp("-", Int(1)))
            For(
              Name("word"),
              Name("words"),
              Assign(
                Name("unique"),
                Call(Name("len"), Call(Name("set"), Name("word"), .Exprs), .Exprs))
              If(
                BoolOp(
                  "or",
                  Compare(Name("unique"), CmpOp(">", Name("max_unique"))),
                  BoolOp(
                    "and",
                    Compare(Name("unique"), CmpOp("==", Name("max_unique"))),
                    Compare(Name("word"), CmpOp("<", Name("result"))),
                    .Exprs),
                  .Exprs),
                Assign(Name("result"), Name("word"))
                Assign(Name("max_unique"), Name("unique"))
                .Stmts,
                .Stmts)
              .Stmts)
            Return(Name("result"))
            .Stmts)))
      ~> Call(
        Name("find_max"),
        list(vCons(str(iCons(97, .IntSeq)), .ValSeq)),
        .Exprs)
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        (.Map
          => "find_max" |-> closureVal(
            "words" , .ParamNames,
            Assign(Name("result"), Str(""))
            Assign(Name("max_unique"), UnaryOp("-", Int(1)))
            Assign(Name("word"), Str(""))
            Assign(Name("unique"), UnaryOp("-", Int(1)))
            For(
              Name("word"),
              Name("words"),
              Assign(
                Name("unique"),
                Call(Name("len"), Call(Name("set"), Name("word"), .Exprs), .Exprs))
              If(
                BoolOp(
                  "or",
                  Compare(Name("unique"), CmpOp(">", Name("max_unique"))),
                  BoolOp(
                    "and",
                    Compare(Name("unique"), CmpOp("==", Name("max_unique"))),
                    Compare(Name("word"), CmpOp("<", Name("result"))),
                    .Exprs),
                  .Exprs),
                Assign(Name("result"), Name("word"))
                Assign(Name("max_unique"), Name("unique"))
                .Stmts,
                .Stmts)
              .Stmts)
            Return(Name("result"))
            .Stmts,
            0)),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
