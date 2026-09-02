requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the correct function returns false on the empty string.
  claim [false-empty-result]:
    <k>
      Call(
        Name("check_if_last_char_is_a_letter"),
        str(.IntSeq), .Exprs)
      => true
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
