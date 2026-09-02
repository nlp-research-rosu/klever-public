requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #loop(
        list(WORDS),
        Name("word"),
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
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        "find_max" |-> closureVal(
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
          0),
        parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "words"      |-> list(ORIGINAL)
        "result"     |-> (BEST:Val => bestWord(WORDS, BEST, SCORE))
        "max_unique" |-> (SCORE => bestScore(WORDS, BEST, SCORE))
        "word"       |-> (CURRENT:Val => lastWord(WORDS, CURRENT))
        "unique"     |-> (CURRENT_SCORE => lastScore(WORDS, CURRENT_SCORE)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <stack> STACK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStrings(WORDS)
         andBool definedProjectStr(BEST)
         andBool notBool isRefV(BEST)

  claim [find-max]:
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
      ~> Call(Name("find_max"), list(WORDS), .Exprs)
      => bestWord(WORDS, str(.IntSeq), 0 -Int 1)
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
    requires allStrings(WORDS)
endmodule
