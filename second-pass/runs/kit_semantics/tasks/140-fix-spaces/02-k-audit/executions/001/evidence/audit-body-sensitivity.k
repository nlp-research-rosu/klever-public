requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // Materially mutate the body actually installed in the claim: initialize
  // result to "X". On empty input the original postcondition "" must fail.
  claim [mutated-body-original-result]:
    <k>
      Call(Name("fix_spaces"), str(.IntSeq))
      =>
      str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fix_spaces" |->
          closureVal(
            ("text", .ParamNames),
            Assign(Name("result"), Str("X"))
            Assign(Name("spaces"), Str(""))
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
