requires "reference-semantics/semantics.k"

module SPEC-BODY-SENSITIVITY
  imports MPY

  // Deliberately mutate the threshold in the loaded function body from 8 to 9.
  // At N=8 this mutated program returns false, so the original true obligation
  // must no longer close.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "is_equal_to_sum_even",
            Params("n"),
            Return(
              BoolOp(
                "and",
                ( Compare(Name("n"), CmpOp(">=", Int(9)))
                , Compare(
                    BinOp("%", Name("n"), Int(2)),
                    CmpOp("==", Int(0)))
                , .Exprs)))
            .Stmts)
          .Stmts))
      ~> Call(Name("is_equal_to_sum_even"), (8, .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        .Map
        => "is_equal_to_sum_even" |->
             closureVal(
               ("n", .ParamNames),
               (Return(
                  BoolOp(
                    "and",
                    ( Compare(Name("n"), CmpOp(">=", Int(9)))
                    , Compare(
                        BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0)))
                    , .Exprs)))
                .Stmts),
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
