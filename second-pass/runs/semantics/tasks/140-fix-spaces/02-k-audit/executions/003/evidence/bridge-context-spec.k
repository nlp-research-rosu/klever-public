requires "verification.k"

module TAIL-CONTEXT-SPEC
  imports FIX-SPACES-BASE

  claim
    <k>
      fixSpacesTailStmt
      ~> Assign(Name("result"), Str("Z"))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(.IntSeq))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 2)
          ("char"   |-> str(.IntSeq)),
          parent(0)))
      (0 |-> scope("fix_spaces" |-> noneV, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(.IntSeq))
          ("result" |-> str(iCons(90, .IntSeq)))
          ("spaces" |-> 2)
          ("char"   |-> str(.IntSeq)),
          parent(0)))
      (0 |-> scope("fix_spaces" |-> noneV, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
endmodule

module STEP-CONTEXT-SPEC
  imports FIX-SPACES-BASE

  claim
    <k>
      fixSpacesLoopBodyStmt
      ~> Assign(Name("result"), Str("Z"))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 2)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |-> scope("fix_spaces" |-> noneV, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, .IntSeq)))
          ("result" |-> str(iCons(90, .IntSeq)))
          ("spaces" |-> 0)
          ("char"   |-> str(iCons(97, .IntSeq))),
          parent(0)))
      (0 |-> scope("fix_spaces" |-> noneV, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
endmodule

module LOOP-CONTEXT-SPEC
  imports FIX-SPACES-BASE

  claim
    <k>
      #loop(
        str(iCons(97, iCons(32, iCons(32, .IntSeq)))),
        Name("char"),
        fixSpacesLoopBody)
      ~> Assign(Name("result"), Str("Z"))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, iCons(32, iCons(32, .IntSeq)))))
          ("result" |-> str(.IntSeq))
          ("spaces" |-> 0)
          ("char"   |-> str(.IntSeq)),
          parent(0)))
      (0 |-> scope("fix_spaces" |-> noneV, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (1 |->
        scope(
          ("text"   |-> str(iCons(97, iCons(32, iCons(32, .IntSeq)))))
          ("result" |-> str(iCons(90, .IntSeq)))
          ("spaces" |-> 2)
          ("char"   |-> str(iCons(32, .IntSeq))),
          parent(0)))
      (0 |-> scope("fix_spaces" |-> noneV, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
endmodule
