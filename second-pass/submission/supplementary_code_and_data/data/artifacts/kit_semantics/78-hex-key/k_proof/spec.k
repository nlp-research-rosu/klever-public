requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [hex-loop]:
    <k>
      #loop(
        str(CS:IntSeq),
        Name("digit"),
        AugAssign(
          Name("count"),
          "+",
          Compare(Name("digit"), CmpOp("in", Str("2357BD")))))
      ~> (Return(Name("count")) .Stmts)
      ~> #endcall
      =>
      (Return(Name("count")) .Stmts)
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(GLOBALS:Map, parent(-1))
       1 |-> scope(
              "num"   |-> str(NUMCS:IntSeq)
              "count" |-> (ACC:Int => ACC +Int hexCount(CS))
              "digit" |-> (DIGIT:Str => ?FINALDIGIT:Str),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [hex-key]:
    <k>
      Call(Name("hex_key"), str(CS:IntSeq))
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
    ensures ?RESULT ==Int hexCount(CS)
endmodule
