requires "verification.k"

// The promoted step rules accept an arbitrary module scope, although the
// bridge-free step claims establish only a module scope containing fix_spaces.
// These ground witnesses shadow ord with a user closure on ordinary string
// inputs.  The fixed semantics must execute the shadowed closure; the promoted
// rules instead assume the builtin ord result.

module BRIDGE-NONSPACE-FIXED-CORRECT
  imports FIX-SPACES-BASE

  claim [nonspace-fixed-correct]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> (0 => 1))
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "ord" |->
            closureVal(
              ("x", .ParamNames),
              Return(Int(32)) .Stmts,
              0),
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

module BRIDGE-NONSPACE-FIXED-WRONG
  imports FIX-SPACES-BASE

  claim [nonspace-fixed-wrong]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> (str(.IntSeq) => str(iCons(97, .IntSeq))))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "ord" |->
            closureVal(
              ("x", .ParamNames),
              Return(Int(32)) .Stmts,
              0),
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

module BRIDGE-NONSPACE-ENABLED-WRONG
  imports FIX-SPACES-STEP-VERIFICATION

  claim [nonspace-enabled-wrong]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> (str(.IntSeq) => str(iCons(97, .IntSeq))))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "ord" |->
            closureVal(
              ("x", .ParamNames),
              Return(Int(32)) .Stmts,
              0),
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

module BRIDGE-SPACE-FIXED-CORRECT
  imports FIX-SPACES-BASE

  claim [space-fixed-correct]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(32, .IntSeq)))
          ("result" |-> (str(.IntSeq) => str(iCons(32, .IntSeq))))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "ord" |->
            closureVal(
              ("x", .ParamNames),
              Return(Int(33)) .Stmts,
              0),
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

module BRIDGE-SPACE-FIXED-WRONG
  imports FIX-SPACES-BASE

  claim [space-fixed-wrong]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(32, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> (0 => 1))
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "ord" |->
            closureVal(
              ("x", .ParamNames),
              Return(Int(33)) .Stmts,
              0),
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

module BRIDGE-SPACE-ENABLED-WRONG
  imports FIX-SPACES-STEP-VERIFICATION

  claim [space-enabled-wrong]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(32, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> (0 => 1))
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "ord" |->
            closureVal(
              ("x", .ParamNames),
              Return(Int(33)) .Stmts,
              0),
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
