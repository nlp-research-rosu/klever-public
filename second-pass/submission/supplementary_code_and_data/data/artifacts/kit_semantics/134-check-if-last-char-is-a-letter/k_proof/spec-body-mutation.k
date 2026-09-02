requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: always return true.  The correct empty-input
  // destination remains false, so an execution-sensitive proof must reject it.
  claim [mutated-body-empty]:
    <k>
      Call(
        Name("check_if_last_char_is_a_letter"),
        str(.IntSeq), .Exprs)
      => standaloneLastLetter(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "check_if_last_char_is_a_letter" |->
               closureVal(
                 "txt", .ParamNames,
                 Return(Bool(true)) .Stmts,
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
