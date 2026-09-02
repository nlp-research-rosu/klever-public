requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: N=3.5 satisfies this start state but returns 0.5, not 0.0.
  claim
    <k> #loadAll(solutionProgram)
         ~> Call(Name("truncate_number"), (Float(N:Float), .Exprs))
      => 0.0 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => 0 |-> scope(
           "truncate_number" |-> closureVal(
             ("number", .ParamNames),
             Return(BinOp("%", Name("number"), Float(1.0))) .Stmts,
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
