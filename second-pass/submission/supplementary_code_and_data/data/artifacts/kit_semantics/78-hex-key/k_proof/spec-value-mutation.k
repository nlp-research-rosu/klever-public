requires "spec.k"

module SPEC-VALUE-MUTATION
  imports SPEC

  claim [two-is-zero]:
    <k>
      Call(Name("hex_key"), str(iCons(50, .IntSeq)))
      =>
      ?RESULT:Int
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "hex_key" |-> closureVal(
                ("num", .ParamNames),
                (Assign(Name("count"), Int(0))
                 Assign(Name("digit"), Str(""))
                 For(
                   Name("digit"),
                   Name("num"),
                   AugAssign(
                     Name("count"),
                     "+",
                     Compare(
                       Name("digit"),
                       CmpOp("in", Str("2357BD")))))
                 Return(Name("count"))),
                0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Int 0
endmodule
