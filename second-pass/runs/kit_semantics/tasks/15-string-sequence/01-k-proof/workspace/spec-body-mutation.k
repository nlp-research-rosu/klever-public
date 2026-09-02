requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated source: "," replaces " " in the loop body while
  // the original stringSequenceCodes postcondition is retained.
  claim [comma-separator]:
    <k>
      Call(Name("string_sequence"), Int(1), .Exprs)
      => str(stringSequenceCodes(1))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "string_sequence" |->
          closureVal(
            "n", .ParamNames,
            Expr(Str("Return space-delimited integers from 0 through n, inclusive."))
            If(
              Compare(Name("n"), CmpOp("<", Int(0))),
              Return(Str("")) .Stmts,
              .Stmts)
            Assign(Name("result"), Str("0"))
            Assign(Name("i"), Int(1))
            While(
              Compare(Name("i"), CmpOp("<=", Name("n"))),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  BinOp("+", Name("result"), Str(",")),
                  Call(Name("str"), Name("i"), .Exprs)))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              .Stmts)
            Return(Name("result"))
            .Stmts,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
