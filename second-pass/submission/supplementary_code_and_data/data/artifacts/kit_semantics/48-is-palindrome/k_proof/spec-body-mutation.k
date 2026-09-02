requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately false: both occurrences of the program body are materially
  // mutated to `return False`, while the empty-string result remains true.
  claim [mutated-body]:
    <k>
      #loadAll(
        Module(
          FuncDef("is_palindrome", Params("text"),
            Return(Bool(false)))
          Assign(
            Name("__result"),
            Call(Name("is_palindrome"), str(.IntSeq)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
          "is_palindrome" |->
            closureVal(
              ("text", .ParamNames),
              Return(Bool(false)) .Stmts,
              0)
          "__result" |-> true,
          parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
