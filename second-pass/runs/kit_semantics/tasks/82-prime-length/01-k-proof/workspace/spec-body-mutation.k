requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The real function returns true on length two. Replacing its entire body by
  // `return False` must make that connection claim fail.
  claim [mutated-length-two]:
    <k>
      Call(
        Name("prime_length"),
        str(iCons(97, iCons(98, .IntSeq))))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "prime_length" |->
          closureVal(
            ("string", .ParamNames),
            (Return(Bool(false)) .Stmts),
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
