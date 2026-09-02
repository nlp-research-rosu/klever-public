requires "verification.k"

module SPEC-BAD-BUILTINS
  imports VERIFICATION

  // Intended-domain input "a", but the builtin scope lacks ord and chr.
  // Fixed semantics gets stuck during lookup; the candidate bridge fabricates "v".
  claim [bad-builtins]:
    <k>
      #loop(str(iCons(97, .IntSeq)), Name("ch"), decodeStep)
    =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "result" |-> str(.IntSeq)
        "ch" |-> str(.IntSeq),
        parent(0))
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> scope(.Map, root)
    =>
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "result" |-> str(iCons(118, .IntSeq))
        "ch" |-> str(iCons(97, .IntSeq)),
        parent(0))
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> scope(.Map, root)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
