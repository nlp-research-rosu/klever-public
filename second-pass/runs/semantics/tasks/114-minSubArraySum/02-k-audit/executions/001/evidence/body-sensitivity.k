requires "verification.k"

module BODY-MUTATION-VERIFICATION
  imports VERIFICATION

  // One material source-body mutation: seed `smallest` with 0 instead of
  // `nums[0]`. All remaining statements, including the real loop body, match.
  syntax Stmts ::= "mutatedMinBody" [macro]
  rule mutatedMinBody =>
       Expr(
         Str(
           "\n    Given an array of integers nums, find the minimum sum of any non-empty\n    sub-array of nums.\n    "))
       Assign(Name("smallest"), Int(0))
       Assign(Name("current"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("nums"), kadaneBody)
       Return(Name("smallest"))
       .Stmts

  syntax Val ::= "mutatedClosure" [macro]
  rule mutatedClosure =>
       closureVal(
         ("nums", .ParamNames),
         mutatedMinBody,
         0)
endmodule

module BODY-SENSITIVITY-SPEC
  imports BODY-MUTATION-VERIFICATION

  // The original program returns 5 on [5]. The mutated program returns 0,
  // so a sound proof must reject this original-result obligation.
  claim
    <k>
      #applyK(
        toCall(mutatedClosure),
        (list(intVals(iCons(5, .IntSeq))), .Vals))
      => 5
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
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
