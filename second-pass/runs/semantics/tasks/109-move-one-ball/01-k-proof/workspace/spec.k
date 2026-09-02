requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive loop summary once Python's loop target has been bound.  The
  // claim is guarded: one concrete semantic iteration occurs before the same
  // claim can be reused for a nonempty tail.
  claim [move-one-ball-loop-induction]:
    <k>
      #loop(list(intVals(iCons(C:Int, IS:IntSeq))),
            Name("current"),
            MOVE-ONE-BALL-LOOP-BODY)
      ~> KONT:K
      =>
      KONT
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> BUILTINS:Scope
      0 |-> MODSCOPE:Scope
      1 |-> scope(
        "arr" |-> ARR:Val
        "drops" |-> D:Int
        "first" |-> F:Int
        "previous" |-> P:Int
        "current" |-> _OLD:Int,
        parent(0))
      =>
      -1 |-> BUILTINS
      0 |-> MODSCOPE
      1 |-> scope(
        "arr" |-> ARR
        "drops" |-> scanDrops(intVals(iCons(C, IS)), P, D)
        "first" |-> F
        "previous" |-> scanLast(intVals(iCons(C, IS)), P)
        "current" |-> scanLast(intVals(iCons(C, IS)), P),
        parent(0))
    </scopes>

  // At loop entry the target name is not yet in the local frame.  One first
  // iteration creates it, after which the induction claim above applies.
  claim [move-one-ball-loop-entry]:
    <k>
      #loop(list(intVals(iCons(C:Int, IS:IntSeq))),
            Name("current"),
            MOVE-ONE-BALL-LOOP-BODY)
      ~> KONT:K
      =>
      KONT
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> BUILTINS:Scope
      0 |-> MODSCOPE:Scope
      1 |-> scope(
        "arr" |-> ARR:Val
        "drops" |-> D:Int
        "first" |-> F:Int
        "previous" |-> P:Int,
        parent(0))
      =>
      -1 |-> BUILTINS
      0 |-> MODSCOPE
      1 |-> scope(
        "arr" |-> ARR
        "drops" |-> scanDrops(intVals(iCons(C, IS)), P, D)
        "first" |-> F
        "previous" |-> scanLast(intVals(iCons(C, IS)), P)
        "current" |-> scanLast(intVals(iCons(C, IS)), P),
        parent(0))
    </scopes>

  // Functional correctness for every finite list of integers.  For a
  // nonempty sequence, moveOneBallSpec counts strict circular descents and
  // accepts exactly when the count is at most one; for empty it is true.
  claim [move-one-ball-correct]:
    <k>
      Call(Name("move_one_ball"), list(intVals(IS:IntSeq)))
      =>
      moveOneBallSpec(intVals(IS))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
              "move_one_ball" |-> MOVE-ONE-BALL-CLOSURE,
              parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
