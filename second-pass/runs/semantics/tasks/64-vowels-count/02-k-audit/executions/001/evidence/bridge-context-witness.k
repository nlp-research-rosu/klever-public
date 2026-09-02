requires "verification.k"

module BRIDGE-CONTEXT-WITNESS-BASE
  imports VOWELS-BASE

  // Ground input "a".  Execution occurs in frame 0, but the candidate bridge
  // incorrectly summarizes frame 1 because its rule omits the <env> guard.
  claim [env-mismatch-base]:
    <k>
      #loop(
        str(iCons(97, .IntSeq)),
        Name("char"),
        vowelLoopBody
      )
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 0
        "char"   |-> str(.IntSeq)
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 0
        "char"   |-> str(.IntSeq)
        "last_y" |-> false,
        parent(0)
      )
      =>
      0 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 0
        "char"   |-> str(.IntSeq)
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 1
        "char"   |-> str(iCons(97, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-CONTEXT-WITNESS-EXTENDED
  imports VOWELS-VERIFICATION

  claim [env-mismatch-extended]:
    <k>
      #loop(
        str(iCons(97, .IntSeq)),
        Name("char"),
        vowelLoopBody
      )
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 0
        "char"   |-> str(.IntSeq)
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 0
        "char"   |-> str(.IntSeq)
        "last_y" |-> false,
        parent(0)
      )
      =>
      0 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 0
        "char"   |-> str(.IntSeq)
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s"      |-> str(iCons(97, .IntSeq))
        "count"  |-> 1
        "char"   |-> str(iCons(97, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
