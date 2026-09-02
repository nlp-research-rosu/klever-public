requires "verification.k"

module AUDITOR-SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false result mutation. For the satisfying input N = 1.5,
  // Python and concrete K both give 1.5 % 1.0 = 0.5, while 1.5 % 2.0 = 1.5.
  claim
    <k> #loadAll(solutionProgram)
         ~> Call(Name("truncate_number"), (Float(N:Float), .Exprs))
      => floatMod(N, 2.0) </k>
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
