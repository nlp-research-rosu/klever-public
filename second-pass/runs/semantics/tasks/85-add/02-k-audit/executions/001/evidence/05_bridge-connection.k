requires "verification-no-bridge.k"

module BRIDGE-CONNECTION
  imports VERIFICATION-NO-BRIDGE

  claim [loop-summary-preserving-empty-stmts]:
    <k>
      #loop(list(intVals(INPUT:IntSeq)), Name("value"), addLoopBody)
      ~> (Return(Name("total")) .Stmts):Stmts
      ~> #endcall
      =>
      (Return(addAccSpec(INPUT, ODD, ACC)) .Stmts):Stmts
      ~> #endcall
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(
        ("lst" |-> LST0:Val)
        ("total" |-> ACC:Int)
        ("odd_index" |-> ODD:Bool)
        ("value" |-> OLDVALUE0:Int),
        PARENT0:Parent))
      RESTSCOPES0:Map
      =>
      (L |-> scope(
        ("total" |-> addAccSpec(INPUT, ODD, ACC))
        ?FINALBINDINGS0:Map,
        PARENT0))
      RESTSCOPES0
    </scopes>
    requires notBool (L in_keys(RESTSCOPES0))

  // A literal one-step connection to the candidate bridge RHS is intentionally
  // not asserted: fixed execution retains an empty Stmts item until Return
  // unwinds the frame. This claim compares the complete observable call effect.
  claim [observable-call-effect]:
    <k>
      #loop(list(intVals(INPUT:IntSeq)), Name("value"), addLoopBody)
      ~> (Return(Name("total")) .Stmts):Stmts
      ~> #endcall
      =>
      addAccSpec(INPUT, false, 0)
      ~> CONT
    </k>
    <env> L:Int => CALLERL:Int </env>
    <scopes>
      (L |-> scope(
        ("lst" |-> list(intVals(INPUT)))
        ("total" |-> 0)
        ("odd_index" |-> false)
        ("value" |-> 0),
        PARENT:Parent))
      RESTSCOPES:Map
      =>
      RESTSCOPES
    </scopes>
    <scopeLoc> CURRENTLOC:Int => SAVEDLOC:Int </scopeLoc>
    <stack>
      ListItem(frame(CONT:K, CALLERL, SAVEDLOC)) RESTSTACK:List
      =>
      RESTSTACK
    </stack>
    <ret> noRet </ret>
    requires notBool (L in_keys(RESTSCOPES))

  claim [exact-loop-summary-with-continuation]:
    <k>
      #loop(list(intVals(INPUT:IntSeq)), Name("value"), addLoopBody)
      ~> (Return(Name("total")) .Stmts):Stmts
      ~> #endcall
      =>
      Return(addAccSpec(INPUT, ODD, ACC))
      ~> #endcall
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(
        ("lst" |-> LST:Val)
        ("total" |-> ACC:Int)
        ("odd_index" |-> ODD:Bool)
        ("value" |-> OLDVALUE:Int),
        PARENT:Parent))
      RESTSCOPES:Map
      =>
      (L |-> scope(
        ("total" |-> addAccSpec(INPUT, ODD, ACC))
        ?FINALBINDINGS:Map,
        PARENT))
      RESTSCOPES
    </scopes>
    requires notBool (L in_keys(RESTSCOPES))
endmodule
