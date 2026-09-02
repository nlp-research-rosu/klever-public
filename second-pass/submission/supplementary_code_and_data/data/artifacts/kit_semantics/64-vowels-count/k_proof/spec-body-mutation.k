requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately false after removing lowercase "u" from the loop condition:
  // this mutated body returns 0 for "u", not the original program's 1.
  claim [mutated-body]:
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
