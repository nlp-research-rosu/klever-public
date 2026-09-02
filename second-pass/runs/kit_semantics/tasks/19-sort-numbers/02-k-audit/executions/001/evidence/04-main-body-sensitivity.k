requires "reference-semantics/semantics.k"

module VERIFICATION-MAIN-BODY-SENSITIVITY
  imports MPY

  // Material mutation: the executed target body returns its input unchanged.
  syntax Val ::= "mutatedSortNumbersClosure" [macro]
  rule mutatedSortNumbersClosure
    => closureVal(
         ("numbers", .ParamNames),
         (Return(Name("numbers")) .Stmts),
         0)
endmodule

module SPEC-MAIN-BODY-SENSITIVITY
  imports VERIFICATION-MAIN-BODY-SENSITIVITY

  claim [mutated-main-sample]:
    <k>
      Call(Name("sort_numbers"), str(strToCodes("three one five")))
      =>
      str(strToCodes("one three five"))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("sort_numbers" |-> mutatedSortNumbersClosure, parent(-1))
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
