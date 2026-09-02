requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Reviewer-authored false obligation. For " a", the last character is the
  // ASCII letter a and its predecessor is a space, so the real body returns
  // true. Requiring false must leave a reachable, result-specific residual.
  claim [false-space-letter-result]:
    <k>
      Call(
        Name("check_if_last_char_is_a_letter"),
        str(iCons(32, iCons(97, .IntSeq))), .Exprs)
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "check_if_last_char_is_a_letter" |->
               closureVal(
                 "txt", .ParamNames,
                 If(
                   Compare(Call(Name("len"), Name("txt")),
                           CmpOp("==", Int(0))),
                   Return(Bool(false)),
                   .Stmts)
                 Return(
                   BoolOp(
                     "and",
                     Call(
                       Attribute(
                         Subscript(Name("txt"), UnaryOp("-", Int(1))),
                         "isalpha"),
                       .Exprs),
                     BoolOp(
                       "or",
                       Compare(Call(Name("len"), Name("txt")),
                               CmpOp("==", Int(1))),
                       Compare(
                         Subscript(Name("txt"), UnaryOp("-", Int(2))),
                         CmpOp("==", Str(" "))),
                       .Exprs),
                     .Exprs)),
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
