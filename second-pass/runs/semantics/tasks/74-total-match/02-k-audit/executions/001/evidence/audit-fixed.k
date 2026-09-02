requires "reference-semantics/semantics.k"

module AUDIT-FIXED
  imports MPY

  syntax StrSeq ::= ".StrSeq"
                  | ssCons(IntSeq, StrSeq)

  syntax ValSeq ::= strVals(StrSeq)
  rule strVals(.StrSeq) => .ValSeq
  rule strVals(ssCons(S:IntSeq, REST:StrSeq))
    => vCons(str(S), strVals(REST))

  syntax KItem ::= nextStrings(StrSeq)
  rule <k> #iterNext(list(strVals(ITEMS:StrSeq)))
        => nextStrings(ITEMS)
        ...
       </k>
       [priority(40)]
  rule <k> nextStrings(.StrSeq)
        => #iterDone
        ...
       </k>
  rule <k> nextStrings(ssCons(S:IntSeq, REST:StrSeq))
        => #iterYield(str(S), list(strVals(REST)))
        ...
       </k>
endmodule
