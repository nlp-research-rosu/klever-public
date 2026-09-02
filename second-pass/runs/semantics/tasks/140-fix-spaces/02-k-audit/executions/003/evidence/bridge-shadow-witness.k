requires "verification.k"

module FIXED-SHADOW-OUTCOME-SPEC
  imports FIX-SPACES-BASE

  // Module-level ord shadows the builtin and always returns 32. Therefore,
  // with char == "a", fixed execution takes the space branch.
  claim
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(32)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 1)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(32)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module FIXED-SHADOW-SPACE-OUTCOME-SPEC
  imports FIX-SPACES-BASE

  // Module-level ord now always returns 97. For char == " ", fixed execution
  // takes the non-space branch, appends the literal space, and leaves N at 0.
  claim
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(32, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(97)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(iCons(32, .IntSeq)))
          ("result" |-> str(iCons(32, .IntSeq)))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(97)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-SHADOW-SPACE-OUTCOME-SPEC
  imports FIX-SPACES-BASE

  // The space bridge ignores that binding and increments N instead.
  claim
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(32, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(97)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(iCons(32, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 1)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(97)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-SHADOW-OUTCOME-SPEC
  imports FIX-SPACES-BASE

  // The candidate bridge's false outcome on the same state: it ignores the
  // module binding, assumes builtin ord("a") == 97, appends "a", and resets.
  claim
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(32)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> str(iCons(97, .IntSeq)))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          ("fix_spaces" |-> noneV)
          ("ord" |-> closureVal("x", Return(Int(32)), 0)),
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
