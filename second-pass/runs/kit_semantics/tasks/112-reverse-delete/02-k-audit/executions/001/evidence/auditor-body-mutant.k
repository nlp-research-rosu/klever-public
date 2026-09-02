requires "verification.k"

module AUDITOR-BODY-MUTANT
  imports VERIFICATION

  // Fresh body sensitivity probe: retain deleted characters instead of
  // non-deleted characters, while demanding the real program's old result.
  claim [changed-condition-old-result]:
    <k>
      Call(
        Name("reverse_delete"),
        ( str(iCons(97, iCons(98, iCons(99, iCons(100, iCons(101, .IntSeq)))))),
          str(iCons(97, iCons(101, .IntSeq))),
          .Exprs))
      => tuple(
           vCons(
             str(iCons(98, iCons(99, iCons(100, .IntSeq)))),
             vCons(false, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "reverse_delete" |->
          closureVal(
            ("s", "c", .ParamNames),
            Assign(Name("result"), Str(""))
            Assign(Name("reversed_result"), Str(""))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              If(
                Compare(Name("ch"), CmpOp("in", Name("c"))),
                AugAssign(Name("result"), "+", Name("ch"))
                Assign(
                  Name("reversed_result"),
                  BinOp("+", Name("ch"), Name("reversed_result"))),
                .Stmts))
            Return(
              TupleExpr(
                Name("result"),
                Compare(
                  Name("result"),
                  CmpOp("==", Name("reversed_result")))))
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
