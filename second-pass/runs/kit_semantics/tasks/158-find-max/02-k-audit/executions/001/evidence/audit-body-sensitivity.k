requires "/tmp/audit-work/reconstruct-001/spec.k"

module AUDIT-BODY-SENSITIVITY
  imports SPEC

  // The program term actually executed below changes max_unique's initializer
  // from -1 to 100 while retaining the original result obligation for ["a"].
  claim [mutated-executed-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "find_max",
            Params("words"),
            Assign(Name("result"), Str(""))
            Assign(Name("max_unique"), Int(100))
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
      => str(iCons(97, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        (.Map
          => "find_max" |-> closureVal(
            "words" , .ParamNames,
            Assign(Name("result"), Str(""))
            Assign(Name("max_unique"), Int(100))
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
