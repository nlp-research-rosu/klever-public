requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the correct result for "abcde" is 2, not 3.
  claim [wrong-result]:
    <k>
      Call(Name("vowels_count"), (Str("abcde"), .Exprs))
      =>
      3
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
               Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))))
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
