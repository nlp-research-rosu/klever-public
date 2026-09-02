requires "verification-body-mutant.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION-BODY-MUTANT

  // The result obligation from the real program must reject this changed body.
  claim
    <k> #loadAll(solutionProgram)
         ~> Call(Name("truncate_number"), (Float(N:Float), .Exprs))
      => floatMod(N, 1.0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => 0 |-> scope(
           "truncate_number" |-> closureVal(
             ("number", .ParamNames),
             Return(Float(0.0)) .Stmts,
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
