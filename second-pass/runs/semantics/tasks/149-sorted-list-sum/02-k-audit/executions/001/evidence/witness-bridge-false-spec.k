requires "verification.k"

module AUDIT-WITNESS-BRIDGE-FALSE-SPEC
  imports HUMANEVAL-VERIFICATION

  // The candidate bridge proves this false fixed-semantics transition.
  claim
    <k>
      #loop(
        list(strVals(INPUT:StrList)),
        Name("word"),
        filterBody)
      ~> Name("word")
    =>
      Name("word")
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
                     "lst" |-> list(strVals(INPUT))
                     "even_words" |-> ref(0),
                     parent(0))
    </scopes>
    <heap>
      ... 0 |-> list(.ValSeq)
    =>
          0 |-> list(evenAppend(.ValSeq, INPUT)) ...
    </heap>
    requires INPUT =/=K .StrList
endmodule
