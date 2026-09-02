requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // Reviewer-authored mutation: the executed closure body is changed to
  // `return True`, while the correct empty-input summary remains false.
  claim [changed-executed-body]:
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
