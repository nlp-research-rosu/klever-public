requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [target-empty]:
    <k>
      Call(
        Name("check_if_last_char_is_a_letter"),
        str(IS:IntSeq), .Exprs)
      => standaloneLastLetter(IS)
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
    requires isLen(IS) ==Int 0

  claim [target-nonalpha]:
    <k>
      Call(
        Name("check_if_last_char_is_a_letter"),
        str(IS:IntSeq), .Exprs)
      => standaloneLastLetter(IS)
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
    requires isLen(IS) >Int 0
      andBool notBool isAlphaC(intSeqAt(IS, isLen(IS) -Int 1))

  claim [target-alpha]:
    <k>
      Call(
        Name("check_if_last_char_is_a_letter"),
        str(IS:IntSeq), .Exprs)
      => standaloneLastLetter(IS)
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
    requires isLen(IS) >Int 0
      andBool isAlphaC(intSeqAt(IS, isLen(IS) -Int 1))
endmodule
