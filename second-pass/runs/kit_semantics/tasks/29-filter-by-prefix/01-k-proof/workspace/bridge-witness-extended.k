requires "verification.k"

module BRIDGE-WITNESS-EXTENDED
  imports VERIFICATION

  claim [iterator-a]:
    <k>
      #iterNext(
        list(
          vCons(
            str(strToCodes("a")),
            .ValSeq)))
      ~> CONT:K
      =>
      #iterYield(
        str(strToCodes("a")),
        list(.ValSeq))
      ~> CONT
    </k>

  claim [iterator-empty]:
    <k>
      #iterNext(
        list(
          vCons(
            str(.IntSeq),
            .ValSeq)))
      ~> CONT:K
      =>
      #iterYield(
        str(.IntSeq),
        list(.ValSeq))
      ~> CONT
    </k>

  claim [loop-keeps]:
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
    <heap>
      0 |-> list(
             .ValSeq
             => vCons(
                  str(strToCodes("abc")),
                  .ValSeq))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [loop-drops]:
    <k>
      #loop(
        list(
          vCons(
            str(strToCodes("bcd")),
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
                    str(strToCodes("bcd")),
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
