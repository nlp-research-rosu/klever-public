requires "../../tmp/audit-work/pairs-audit/verification.k"

module AUDIT-BRIDGE-FIXED
  imports PAIRS-VERIFICATION

  // Ordinary fixed-semantics result for the real empty-list input.
  claim [real-empty-fixed-heap]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(.ValSeq), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Deliberately false under fixed semantics: this is the heap fabricated by
  // the proof-local empty-list bridge.
  claim [real-empty-synthetic-heap]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(.ValSeq), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(intValues(.IntSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-BRIDGE-EXTENDED
  imports PAIRS-VERIFICATION-LEMMAS

  // The proof-local priority rule makes the false fixed-semantics heap
  // conclusion provable for the same real empty-list input.
  claim [real-empty-synthetic-heap]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(.ValSeq), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(intValues(.IntSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
