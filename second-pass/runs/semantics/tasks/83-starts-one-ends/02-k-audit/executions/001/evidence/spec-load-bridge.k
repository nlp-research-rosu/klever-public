requires "verification.k"

module SPEC-LOAD-BRIDGE
  imports VERIFICATION

  claim
    <k>
      #loadAll(
        Module(
          FuncDef("starts_one_ends", Params("n"),
            Expr(
              Str(
                "\n    Given a positive integer n, return the count of the numbers of n-digit\n    positive integers that start or end with 1.\n    "))
            If(Compare(Name("n"), CmpOp("==", Int(1))),
              Return(Int(1)),
              .Stmts)
            Return(
              BinOp(
                "*",
                Int(18),
                BinOp("**", Int(10), BinOp("-", Name("n"), Int(2))))))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "starts_one_ends" |->
          closureVal(("n", .ParamNames), startsOneEndsBody, 0),
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
