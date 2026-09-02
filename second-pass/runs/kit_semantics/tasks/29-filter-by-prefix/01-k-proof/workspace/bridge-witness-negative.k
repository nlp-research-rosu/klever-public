requires "verification.k"

module BRIDGE-WITNESS-NEGATIVE
  imports VERIFICATION

  claim [wrong-iterator-value]:
    <k>
      #iterNext(
        list(
          vCons(
            str(strToCodes("a")),
            .ValSeq)))
      =>
      #iterYield(
        str(.IntSeq),
        list(.ValSeq))
    </k>

  claim [wrong-loop-value]:
    <k>
      #loop(
        list(
          vCons(
            str(strToCodes("abc")),
            .ValSeq)),
        Name("string"),
        filterLoopBody)
      ~> (Return(Name("result")) .Stmts):Stmts
      ~> #endcall
      => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(
              "strings" |->
                list(
                  vCons(
                    str(strToCodes("abc")),
                    .ValSeq))
              "prefix" |-> str(strToCodes("a"))
              "result" |-> ref(0)
              "string" |-> str(.IntSeq),
              parent(0)))
      => SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
