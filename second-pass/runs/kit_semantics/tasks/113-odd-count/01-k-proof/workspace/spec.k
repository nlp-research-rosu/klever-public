requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [outer-loop-cons]:
    <k>
      #loop(
        list(vCons(HEAD:Val, REST:ValSeq)),
        Name("s"),
        ODD-COUNT-LOOP-BODY)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "count" |-> (COUNT:Int => ?COUNT:Int)
        "count_string" |-> (str(COUNTSTRING:IntSeq) => str(?COUNTSTRING:IntSeq))
        "lst" |-> list(INPUT:ValSeq)
        "result" |-> ref(0)
        "s" |-> (S:Val => ?S:Val),
        parent(0))
      0 |-> scope(
        "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(
        ACC:ValSeq
        =>
        oddLinesAcc(ACC, vCons(HEAD, REST)))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigitStrings(vCons(HEAD, REST))

  claim [odd-count-empty]:
    <k>
      Call(Name("odd_count"), list(.ValSeq))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [odd-count-cons]:
    <k>
      Call(
        Name("odd_count"),
        list(vCons(HEAD:Val, REST:ValSeq)))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        oddLinesAcc(
          .ValSeq,
          vCons(HEAD, REST)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigitStrings(vCons(HEAD, REST))
endmodule
