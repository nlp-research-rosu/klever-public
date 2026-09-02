requires "verification.k"

module FIX-SPACES-FLUSH-SPEC
  imports FIX-SPACES-BASE

  claim [flush-zero]:
    <k> fixSpacesTailStmt => .K </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> 0)
          ("char"   |-> str(CH:IntSeq)),
          parent(0))
      =>
      1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(A))
          ("spaces" |-> 0)
          ("char"   |-> str(CH)),
          parent(0))
      ...
    </scopes>

  claim [flush-one]:
    <k> fixSpacesTailStmt => .K </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> 1)
          ("char"   |-> str(CH:IntSeq)),
          parent(0))
      =>
      1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(seqConcat(A, iCons(95, .IntSeq))))
          ("spaces" |-> 1)
          ("char"   |-> str(CH)),
          parent(0))
      ...
    </scopes>

  claim [flush-two]:
    <k> fixSpacesTailStmt => .K </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> 2)
          ("char"   |-> str(CH:IntSeq)),
          parent(0))
      =>
      1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |->
            str(
              seqConcat(
                A,
                iCons(95, iCons(95, .IntSeq)))))
          ("spaces" |-> 2)
          ("char"   |-> str(CH)),
          parent(0))
      ...
    </scopes>

  claim [flush-many]:
    <k> fixSpacesTailStmt => .K </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(CH:IntSeq)),
          parent(0))
      =>
      1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(seqConcat(A, iCons(45, .IntSeq))))
          ("spaces" |-> N)
          ("char"   |-> str(CH)),
          parent(0))
      ...
    </scopes>
    requires N >Int 2
endmodule

module FIX-SPACES-STEP-SPEC
  imports FIX-SPACES-FLUSH-VERIFICATION

  claim [step-space]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION:Val,
          parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(A))
          ("spaces" |-> N +Int 1)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION,
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    requires N >=Int 0

  claim [step-non-space]:
    <k> fixSpacesLoopBodyStmt => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(iCons(C:Int, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION:Val,
          parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |->
            str(
              seqConcat(
                appendPending(A, N),
                iCons(C, .IntSeq))))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(C, .IntSeq))),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION,
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    requires N >=Int 0 andBool C =/=Int 32
endmodule

module FIX-SPACES-LOOP-SPEC
  imports FIX-SPACES-STEP-VERIFICATION

  // Structural induction over IS proves the exact loop summary used below.
  claim
    <k>
      #loop(str(IS:IntSeq), Name("char"), fixSpacesLoopBody)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(TEXT:IntSeq))
          ("result" |-> str(A:IntSeq))
          ("spaces" |-> N:Int)
          ("char"   |-> str(CH:IntSeq)),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION:Val,
          parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(TEXT))
          ("result" |-> str(fixSpacesLoop(A, IS, N)))
          ("spaces" |-> trailingSpaces(IS, N))
          ("char"   |-> str(finalChar(IS, CH))),
          parent(0)))
      (0 |->
        scope(
          "fix_spaces" |-> FUNCTION,
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    requires N >=Int 0
endmodule

module FIX-SPACES-MAIN-SPEC
  imports FIX-SPACES-VERIFICATION

  // End-to-end functional correctness from the translated function body.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("fix_spaces"), str(IS:IntSeq))
      =>
      str(
        appendPending(
          fixSpacesLoop(.IntSeq, IS, 0),
          trailingSpaces(IS, 0)))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |->
        scope(
          "fix_spaces" |->
            closureVal("text", fixSpacesFunctionBody, 0),
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
