requires "verification.k"

module SPEC-BODY-SENSITIVITY-AUDIT
  imports VERIFICATION

  // Fresh body mutation: delete lowercase u from the executed membership
  // literal, but retain the original obligation for concrete input "u".
  claim [fresh-mutated-body]:
    <k>
      Call(Name("vowels_count"), (Str("u"), .Exprs))
      =>
      1
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
         "vowels_count" |-> closureVal(
           ("s", .ParamNames),
           Assign(Name("count"), Int(0))
           Assign(Name("last"), Str(""))
           Assign(Name("char"), Str(""))
           For(
             Name("char"),
             Name("s"),
             AugAssign(
               Name("count"),
               "+",
               Compare(Name("char"), CmpOp("in", Str("aeioAEIOU"))))
             Assign(Name("last"), Name("char"))
             .Stmts)
           AugAssign(
             Name("count"),
             "+",
             Compare(Name("last"), CmpOp("==", Str("y"))))
           AugAssign(
             Name("count"),
             "+",
             Compare(Name("last"), CmpOp("==", Str("Y"))))
           Return(Name("count"))
           .Stmts,
           0),
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
