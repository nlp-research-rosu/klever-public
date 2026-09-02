requires "verification.k"

// The proof-local bridge returns the right abstract string but skips both list
// allocations performed by list(word) and sorted(...).
module SORT-BRIDGE-FALSE-EXTENDED
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  claim <k>
    Call(
      Attribute(Str(""), "join"),
      Call(Name("sorted"), Call(Name("list"), Name("word"))))
    =>
    str(sortWord(iCons(98, iCons(97, .IntSeq))))
  </k>
  <env> 1 </env>
  <scopes>
    1 |-> scope(
      "word" |-> str(iCons(98, iCons(97, .IntSeq))),
      parent(0))
    0  |-> scope(.Map, parent(-1))
    -1 |-> builtinsScope
  </scopes>
  <heap> .Map </heap>
  <heapLoc> 0 </heapLoc>
endmodule

// Under the supplied semantics, the same no-allocation conclusion is false.
module SORT-BRIDGE-FALSE-BASE
  imports ANTI-SHUFFLE-BASE

  claim <k>
    Call(
      Attribute(Str(""), "join"),
      Call(Name("sorted"), Call(Name("list"), Name("word"))))
    =>
    str(sortWord(iCons(98, iCons(97, .IntSeq))))
  </k>
  <env> 1 </env>
  <scopes>
    1 |-> scope(
      "word" |-> str(iCons(98, iCons(97, .IntSeq))),
      parent(0))
    0  |-> scope(.Map, parent(-1))
    -1 |-> builtinsScope
  </scopes>
  <heap> .Map </heap>
  <heapLoc> 0 </heapLoc>
endmodule

// This is the actual supplied-semantics state transition for the same call.
module SORT-BRIDGE-TRUE-BASE
  imports ANTI-SHUFFLE-BASE

  claim <k>
    Call(
      Attribute(Str(""), "join"),
      Call(Name("sorted"), Call(Name("list"), Name("word"))))
    =>
    str(sortWord(iCons(98, iCons(97, .IntSeq))))
  </k>
  <env> 1 </env>
  <scopes>
    1 |-> scope(
      "word" |-> str(iCons(98, iCons(97, .IntSeq))),
      parent(0))
    0  |-> scope(.Map, parent(-1))
    -1 |-> builtinsScope
  </scopes>
  <heap>
    .Map
    =>
    0 |-> list(charsOf(iCons(98, iCons(97, .IntSeq))))
    1 |-> list(sortVS(charsOf(iCons(98, iCons(97, .IntSeq)))))
  </heap>
  <heapLoc> 0 => 2 </heapLoc>
endmodule
