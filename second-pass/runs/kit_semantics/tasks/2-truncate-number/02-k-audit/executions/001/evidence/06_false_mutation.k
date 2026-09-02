requires "verification.k"

module AUDITOR-FALSE-RESULT
  imports VERIFICATION

  // Deliberately false: at F = 3.5 the actual result is 0.5, not 3.5.
  claim [false-identity-result]:
    <k> Call(Name("truncate_number"), (F:Float, .Exprs))
        => F
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map [
          "truncate_number" <-
            closureVal(
              ("number", .ParamNames),
              (Return(BinOp("%", Name("number"), Float(1.0))) .Stmts),
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
