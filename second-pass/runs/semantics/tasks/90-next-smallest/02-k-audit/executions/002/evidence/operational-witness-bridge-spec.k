requires "verification.k"

module OPERATIONAL-WITNESS-BRIDGE-SPEC
  imports NEXT-SMALLEST-WITH-LOOP-LEMMA

  claim
    <k>
      #loop(
        list(intVals(consInts(3, consInts(1, consInts(2, consInts(1, nilInts)))))),
        Name("value"),
        nextSmallestLoopBody)
      ~> nextSmallestReturn
      ~> #endcall
    =>
      2
    </k>
    <env> 1 => 0 </env>
    <scopes>
      1 |-> scope(
        ("value" |-> 0
         "lst" |-> list(intVals(consInts(3, consInts(1, consInts(2, consInts(1, nilInts))))))
         "smallest" |-> 0
         "second" |-> 0
         "count" |-> 0),
        parent(0))
    =>
      .Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
