requires "reference-semantics/semantics.k"

module SPEC-FIXED-REAL-PROGRAM
  imports MPY

  // Bridge-free fixed-semantics check: load the actual submitted Module/FuncDef,
  // resolve its bound name, and call it for an arbitrary mathematical integer.
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
                ( Compare(Name("n"), CmpOp(">=", Int(8)))
                , Compare(
                    BinOp("%", Name("n"), Int(2)),
                    CmpOp("==", Int(0)))
                , .Exprs)))
            .Stmts)
          .Stmts))
      ~> Call(Name("is_equal_to_sum_even"), (N:Int, .Exprs))
      => (N >=Int 8 andBool pyMod(N, 2) ==Int 0)
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
                    ( Compare(Name("n"), CmpOp(">=", Int(8)))
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
