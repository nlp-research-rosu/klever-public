requires "verification.k"

module TOTAL-MATCH-LOOP-SPEC
  imports TOTAL-MATCH-VERIFICATION

  // Independent induction proof for the summary used by the program claims.
  // The arbitrary OLD value generalizes the loop-variable binding between
  // iterations.  The proof-only observer reads the accumulator and removes
  // that unobservable binding at the end.
  claim
    <k>
      #loop(
        list(strVals(ITEMS:StrSeq)),
        Name("item"),
        AugAssign(
          Name("acc"),
          "+",
          Call(Name("len"), Name("item"))) .Stmts)
      ~> readAccAndDrop("acc", "item")
      => I +Int totalChars(ITEMS)
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
      1  |-> scope(
        (("acc" |-> I:Int) ("item" |-> OLD:Val)
          => "acc" |-> (I +Int totalChars(ITEMS))),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

module TOTAL-MATCH-SPEC
  imports TOTAL-MATCH-VERIFICATION

  claim
    <k> runTotalMatch(A:StrSeq, B:StrSeq)
      => list(strVals(A))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires totalChars(A) <=Int totalChars(B)

  claim
    <k> runTotalMatch(A:StrSeq, B:StrSeq)
      => list(strVals(B))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires totalChars(A) >Int totalChars(B)
endmodule
