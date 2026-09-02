requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: reverse_delete("", "") returns ("", true).
  claim [false-result]:
    <k>
      Call(
        Name("reverse_delete"),
        (str(.IntSeq), str(.IntSeq), .Exprs))
      => tuple(vCons(str(.IntSeq), vCons(false, .ValSeq)))
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
                Compare(Name("ch"), CmpOp("not in", Name("c"))),
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
