requires "verification-body-mutation.k"

module AUDITOR-SPEC-BODY-MUTATION
  imports AUDITOR-VERIFICATION-BODY-MUTATION

  // Keep the original result obligation while changing the executed body.
  claim
    <k> #loadAll(mutatedSolutionProgram)
         ~> Call(Name("truncate_number"), (Float(N:Float), .Exprs))
      => floatMod(N, 1.0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => 0 |-> scope(
           "truncate_number" |-> closureVal(
             ("number", .ParamNames),
             Return(BinOp("+", Name("number"), Float(1.0))) .Stmts,
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
