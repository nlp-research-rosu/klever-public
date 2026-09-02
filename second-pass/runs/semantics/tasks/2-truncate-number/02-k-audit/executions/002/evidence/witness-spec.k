requires "verification.k"

module AUDITOR-WITNESS-SPEC
  imports VERIFICATION

  // Satisfiable ground instance of the entry claim: N = 3.5.
  claim
    <k> #loadAll(solutionProgram)
         ~> Call(Name("truncate_number"), (Float(3.5), .Exprs))
      => 0.5 </k>
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
