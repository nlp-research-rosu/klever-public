requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim [changed-body]:
    <k> Call(Name("truncate_number"), (F:Float, .Exprs))
        => floatMod(F, 1.0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map [
          "truncate_number" <-
            closureVal(
              ("number", .ParamNames),
              (Return(BinOp("%", Name("number"), Float(2.0))) .Stmts),
              0
            )
        ],
        parent(-1)
      )
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
