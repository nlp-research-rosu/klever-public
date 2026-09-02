requires "verification.k"

module SPEC
  imports VERIFICATION

  // For an arbitrary floating-point input, executing the translated function
  // returns exactly the semantics' Python floor-modulo primitive.  The
  // supplied semantics evaluates that primitive concretely as
  // n - floor(n / 1.0) * 1.0, i.e. the requested decimal part for n > 0.
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
