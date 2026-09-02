requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The material mutation initializes spaces to "-" instead of "".
  // For text == "", the mutated body returns "-", so the original result fails.
  claim [mutated-body]:
    <k>
      Call(Name("fix_spaces"), str(.IntSeq))
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "fix_spaces" |->
                 closureVal(
                   ("text", .ParamNames),
                   Assign(Name("result"), Str(""))
                   Assign(Name("spaces"), Str("-"))
                   Assign(Name("char"), Str(""))
                   For(Name("char"), Name("text"), #fixSpacesLoopBody)
                   Return(BinOp("+", Name("result"), Name("spaces"))),
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
