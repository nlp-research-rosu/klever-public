requires "verification.k"

module BRIDGE-BUILTIN-WITNESS
  imports VERIFICATION

  // Intended-domain input "a" (code 97), but an empty root builtins scope.
  // Fixed execution cannot resolve ord/chr and therefore cannot reach the
  // asserted successful decode. The candidate loop lemma accepts this scope
  // through BUILTINS:Scope and fabricates the successful state.
  claim [bad-builtins-success]:
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
