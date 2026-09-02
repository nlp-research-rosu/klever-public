requires "verification.k"

// The submitted loop theorem proves only the continuation Name("result").
// The installed rule accepts every continuation and leaves "word" unchanged.
module LOOP-BRIDGE-FALSE-EXTENDED
  imports ANTI-SHUFFLE-VERIFICATION

  claim <k>
    #loop(
      wordsObj(wCons(iCons(98, iCons(97, .IntSeq)), .Words)),
      Name("word"),
      antiLoopBody)
    ~> Name("word")
    =>
    str(.IntSeq)
  </k>
  <env> 1 </env>
  <scopes>
    1 |-> scope(
      "result" |-> str(.IntSeq)
      "s"      |-> str(iCons(98, iCons(97, .IntSeq)))
      "word"   |-> str(.IntSeq),
      parent(0))
    0  |-> scope(.Map, parent(-1))
    -1 |-> builtinsScope
    =>
    ?SCEXT:Map
  </scopes>
  <heap> .Map </heap>
  <heapLoc> 0 </heapLoc>
endmodule

// Without the installed summary, the loop binds "word" to "ba", so the same
// false postcondition must be rejected.
module LOOP-BRIDGE-FALSE-BASE
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  claim <k>
    #loop(
      wordsObj(wCons(iCons(98, iCons(97, .IntSeq)), .Words)),
      Name("word"),
      antiLoopBody)
    ~> Name("word")
    =>
    str(.IntSeq)
  </k>
  <env> 1 </env>
  <scopes>
    1 |-> scope(
      "result" |-> str(.IntSeq)
      "s"      |-> str(iCons(98, iCons(97, .IntSeq)))
      "word"   |-> str(.IntSeq),
      parent(0))
    0  |-> scope(.Map, parent(-1))
    -1 |-> builtinsScope
    =>
    ?SCBASE:Map
  </scopes>
  <heap> .Map </heap>
  <heapLoc> 0 </heapLoc>
endmodule
