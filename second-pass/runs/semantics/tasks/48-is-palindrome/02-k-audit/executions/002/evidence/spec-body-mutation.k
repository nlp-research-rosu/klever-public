requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity probe: the claim executes a materially changed body.
  // The final scope is updated too, so failure must come from the returned value.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "is_palindrome",
            Params("text"),
            Return(Bool(false))
            .Stmts)))
      ~> Call(Name("is_palindrome"), str(IS:IntSeq))
    =>
      palindrome(IS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(
        "is_palindrome" |->
          closureVal(
            "text",
            Return(Bool(false))
            .Stmts,
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
